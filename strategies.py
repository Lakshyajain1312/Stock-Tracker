import pandas as pd
import numpy as np
import yfinance as yf
from typing import Optional, Dict, Tuple

class MomentumStrategy:
    """
    Momentum strategy implementation based on rolling returns and trend analysis.
    """
    
    def __init__(self, lookback_period: int = 60):
        self.lookback_period = lookback_period
    
    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate momentum strategy signals and returns.
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            DataFrame with momentum signals and cumulative returns
        """
        if data.empty or len(data) < self.lookback_period:
            return pd.DataFrame()
        
        df = data.copy()
        
        # Calculate rolling returns
        df['returns'] = df['Close'].pct_change()
        df['rolling_return'] = df['returns'].rolling(window=self.lookback_period).sum()
        
        # Calculate momentum indicators
        df['price_ma'] = df['Close'].rolling(window=self.lookback_period).mean()
        df['momentum_ratio'] = df['Close'] / df['price_ma']
        
        # Generate signals
        # Buy when momentum is positive and price is above moving average
        df['signal'] = np.where(
            (df['rolling_return'] > 0) & (df['momentum_ratio'] > 1.02), 1,
            np.where(
                (df['rolling_return'] < 0) | (df['momentum_ratio'] < 0.98), -1, 0
            )
        )
        
        # Forward fill signals to avoid frequent switching
        df['signal'] = df['signal'].replace(0, np.nan).ffill().fillna(0)
        
        # Calculate strategy returns
        df['strategy_return'] = df['signal'].shift(1) * df['returns']
        df['cumulative_return'] = (1 + df['strategy_return'].fillna(0)).cumprod() - 1
        
        # Clean up and return relevant columns
        result = df[['signal', 'strategy_return', 'cumulative_return', 'momentum_ratio', 'rolling_return']].copy()
        result = result.dropna()
        
        return result

class ValueStrategy:
    """
    Value strategy implementation based on mean reversion and relative valuation.
    """
    
    def __init__(self, lookback_period: int = 252):
        self.lookback_period = lookback_period
    
    def calculate(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate value strategy signals and returns.
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            DataFrame with value signals and cumulative returns
        """
        if data.empty or len(data) < self.lookback_period:
            return pd.DataFrame()
        
        df = data.copy()
        
        # Calculate returns
        df['returns'] = df['Close'].pct_change()
        
        # Calculate value indicators
        df['long_ma'] = df['Close'].rolling(window=self.lookback_period).mean()
        df['short_ma'] = df['Close'].rolling(window=self.lookback_period//4).mean()
        df['value_ratio'] = df['Close'] / df['long_ma']
        
        # Calculate volatility-adjusted metrics
        df['volatility'] = df['returns'].rolling(window=60).std()
        df['bollinger_upper'] = df['long_ma'] + (2 * df['volatility'] * df['Close'])
        df['bollinger_lower'] = df['long_ma'] - (2 * df['volatility'] * df['Close'])
        
        # Calculate RSI-like momentum for contrarian signals
        price_changes = df['Close'].diff()
        gains = price_changes.where(price_changes > 0, 0)
        losses = -price_changes.where(price_changes < 0, 0)
        avg_gains = gains.rolling(window=14).mean()
        avg_losses = losses.rolling(window=14).mean()
        rs = avg_gains / avg_losses
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # Generate value-based signals
        # Buy when price is significantly below long-term average (undervalued)
        # and RSI indicates oversold conditions
        buy_condition = (
            (df['value_ratio'] < 0.95) &  # Price below 95% of long-term average
            (df['rsi'] < 30) &  # Oversold condition
            (df['short_ma'] < df['long_ma'])  # Confirming downtrend
        )
        
        # Sell when price is significantly above long-term average (overvalued)
        # and RSI indicates overbought conditions
        sell_condition = (
            (df['value_ratio'] > 1.05) &  # Price above 105% of long-term average
            (df['rsi'] > 70) &  # Overbought condition
            (df['short_ma'] > df['long_ma'])  # Confirming uptrend
        )
        
        df['signal'] = np.where(buy_condition, 1,
                               np.where(sell_condition, -1, 0))
        
        # Forward fill signals to avoid frequent switching
        df['signal'] = df['signal'].replace(0, np.nan).ffill().fillna(0)
        
        # Calculate strategy returns
        df['strategy_return'] = df['signal'].shift(1) * df['returns']
        df['cumulative_return'] = (1 + df['strategy_return'].fillna(0)).cumprod() - 1
        
        # Clean up and return relevant columns
        result = df[['signal', 'strategy_return', 'cumulative_return', 'value_ratio', 'rsi']].copy()
        result = result.dropna()
        
        return result

class StrategyComparison:
    """
    Utility class for comparing strategy performances.
    """
    
    @staticmethod
    def calculate_metrics(strategy_data: pd.DataFrame) -> dict:
        """
        Calculate performance metrics for a strategy.
        
        Args:
            strategy_data: DataFrame with strategy returns
            
        Returns:
            Dictionary with performance metrics
        """
        if strategy_data.empty or 'strategy_return' not in strategy_data.columns:
            return {}
        
        returns = strategy_data['strategy_return'].dropna()
        
        if len(returns) == 0:
            return {}
        
        total_return = strategy_data['cumulative_return'].iloc[-1] if 'cumulative_return' in strategy_data else 0
        volatility = returns.std() * np.sqrt(252)  # Annualized
        sharpe_ratio = (returns.mean() * 252) / volatility if volatility > 0 else 0
        
        # Calculate maximum drawdown
        cumulative = (1 + returns).cumprod()
        rolling_max = cumulative.expanding().max()
        drawdown = (cumulative - rolling_max) / rolling_max
        max_drawdown = drawdown.min()
        
        # Win rate
        positive_returns = returns[returns > 0]
        win_rate = len(positive_returns) / len(returns) if len(returns) > 0 else 0
        
        return {
            'total_return': total_return,
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'win_rate': win_rate,
            'number_of_trades': len(returns[returns != 0])
        }
    
    @staticmethod
    def compare_strategies(momentum_data: pd.DataFrame, value_data: pd.DataFrame) -> pd.DataFrame:
        """
        Compare momentum and value strategies side by side.
        
        Args:
            momentum_data: Momentum strategy results
            value_data: Value strategy results
            
        Returns:
            DataFrame with comparison metrics
        """
        momentum_metrics = StrategyComparison.calculate_metrics(momentum_data)
        value_metrics = StrategyComparison.calculate_metrics(value_data)
        
        comparison = pd.DataFrame({
            'Momentum': momentum_metrics,
            'Value': value_metrics
        }).T
        
        return comparison

class KeyMetricsCalculator:
    """
    Calculate comprehensive key metrics with formulas for stocks and benchmarks.
    """
    
    @staticmethod
    def calculate_comprehensive_metrics(data: pd.DataFrame, symbol: str) -> Dict:
        """
        Calculate all key metrics with formulas and values.
        
        Args:
            data: DataFrame with OHLCV data
            symbol: Stock/benchmark symbol
            
        Returns:
            Dictionary with metrics, formulas, and values
        """
        if data.empty:
            return {}
        
        try:
            # Basic price data
            opening_price = data['Open'].iloc[0]
            closing_price = data['Close'].iloc[-1]
            current_price = closing_price
            
            # Calculate daily returns
            returns = data['Close'].pct_change().dropna()
            
            # 1. Average Price
            avg_price = (opening_price + closing_price) / 2
            
            # 2. Cumulative Return
            cumulative_return = (closing_price / opening_price) - 1
            
            # 3. Sharpe Ratio
            if len(returns) > 1:
                mean_return = returns.mean()
                std_return = returns.std()
                sharpe_ratio = (mean_return / std_return) * np.sqrt(252) if std_return > 0 else 0
            else:
                sharpe_ratio = 0
            
            # 4. Max Drawdown
            cumulative_values = (1 + returns).cumprod()
            rolling_max = cumulative_values.expanding().max()
            drawdown = (cumulative_values - rolling_max) / rolling_max
            max_drawdown = drawdown.min()
            
            # Get additional metrics from yfinance (P/E, P/B, Dividend Yield)
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                
                pe_ratio = info.get('trailingPE', 'N/A')
                pb_ratio = info.get('priceToBook', 'N/A')
                dividend_yield = info.get('dividendYield', 'N/A')
                if isinstance(dividend_yield, (int, float)):
                    dividend_yield = dividend_yield * 100  # Convert to percentage
                
            except Exception:
                pe_ratio = 'N/A'
                pb_ratio = 'N/A'
                dividend_yield = 'N/A'
            
            # Format results with formulas
            metrics = {
                'Average Price': {
                    'formula': 'Average Price = (Opening Price on first day + Closing Price on last day) ÷ 2',
                    'calculation': f'({opening_price:.2f} + {closing_price:.2f}) ÷ 2',
                    'value': f'${avg_price:.2f}',
                    'raw_value': avg_price
                },
                'Cumulative Return': {
                    'formula': 'Cumulative Return = (Final Price ÷ Initial Price) - 1',
                    'calculation': f'({closing_price:.2f} ÷ {opening_price:.2f}) - 1',
                    'value': f'{cumulative_return:.2%}',
                    'raw_value': cumulative_return
                },
                'Sharpe Ratio': {
                    'formula': 'Sharpe Ratio = (Mean(Returns) ÷ Std(Returns)) × √252',
                    'calculation': f'({returns.mean():.6f} ÷ {returns.std():.6f}) × √252' if len(returns) > 1 else 'Insufficient data',
                    'value': f'{sharpe_ratio:.2f}',
                    'raw_value': sharpe_ratio
                },
                'Max Drawdown': {
                    'formula': 'Max Drawdown = (Trough Value – Peak Value) ÷ Peak Value',
                    'calculation': f'Minimum of rolling drawdowns',
                    'value': f'{max_drawdown:.2%}',
                    'raw_value': max_drawdown
                },
                'P/E Ratio': {
                    'formula': 'P/E Ratio = Price ÷ Earnings per Share',
                    'calculation': f'Current Price ÷ EPS (from financial data)',
                    'value': f'{pe_ratio:.2f}' if isinstance(pe_ratio, (int, float)) else str(pe_ratio),
                    'raw_value': pe_ratio
                },
                'P/B Ratio': {
                    'formula': 'P/B Ratio = Price ÷ Book Value per Share',
                    'calculation': f'Current Price ÷ Book Value per Share',
                    'value': f'{pb_ratio:.2f}' if isinstance(pb_ratio, (int, float)) else str(pb_ratio),
                    'raw_value': pb_ratio
                },
                'Dividend Yield': {
                    'formula': 'Dividend Yield = Annual Dividends ÷ Price × 100%',
                    'calculation': f'Annual Dividends ÷ Current Price × 100%',
                    'value': f'{dividend_yield:.2f}%' if isinstance(dividend_yield, (int, float)) else str(dividend_yield),
                    'raw_value': dividend_yield
                }
            }
            
            return metrics
            
        except Exception as e:
            return {'error': f'Error calculating metrics: {str(e)}'}
    
    @staticmethod
    def format_metrics_for_display(metrics: Dict, asset_name: str) -> str:
        """
        Format metrics for display in Streamlit expander.
        
        Args:
            metrics: Dictionary from calculate_comprehensive_metrics
            asset_name: Name of the asset
            
        Returns:
            Formatted string for display
        """
        if not metrics or 'error' in metrics:
            return f"❌ Unable to calculate metrics for {asset_name}"
        
        display_text = f"### 📊 Key Metrics for {asset_name}\n\n"
        
        for metric_name, metric_data in metrics.items():
            display_text += f"**{metric_name}**\n"
            display_text += f"- *Formula*: {metric_data['formula']}\n"
            display_text += f"- *Calculation*: {metric_data['calculation']}\n"
            display_text += f"- *Value*: **{metric_data['value']}**\n\n"
        
        return display_text
