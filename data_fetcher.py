import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, date
from typing import Optional
import streamlit as st

class DataFetcher:
    """
    Utility class for fetching and processing stock market data using yfinance.
    """
    
    def __init__(self):
        self.cache = {}
    
    def get_stock_data(self, symbol: str, start_date: date, end_date: date) -> pd.DataFrame:
        """
        Fetch stock data from Yahoo Finance.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'RELIANCE.NS')
            start_date: Start date for data
            end_date: End date for data
            
        Returns:
            DataFrame with OHLCV data
        """
        try:
            # Create cache key
            cache_key = f"{symbol}_{start_date}_{end_date}"
            
            # Check cache first
            if cache_key in self.cache:
                return self.cache[cache_key]
            
            # Fetch data from yfinance
            ticker = yf.Ticker(symbol)
            data = ticker.history(start=start_date, end=end_date)
            
            if data.empty:
                st.error(f"No data found for symbol: {symbol}")
                return pd.DataFrame()
            
            # Clean and validate data
            data = self._clean_data(data)
            
            # Cache the result
            self.cache[cache_key] = data
            
            return data
            
        except Exception as e:
            st.error(f"Error fetching data for {symbol}: {str(e)}")
            return pd.DataFrame()
    
    def _clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and validate stock data.
        
        Args:
            data: Raw stock data from yfinance
            
        Returns:
            Cleaned DataFrame
        """
        # Remove any rows with missing data
        data = data.dropna()
        
        # Ensure we have required columns
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing_columns = [col for col in required_columns if col not in data.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Remove any rows with zero or negative prices
        data = data[(data['Close'] > 0) & (data['Volume'] > 0)]
        
        # Sort by date
        data = data.sort_index()
        
        return data
    
    def get_stock_info(self, symbol: str) -> dict:
        """
        Get basic information about a stock.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Dictionary with stock information
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'name': info.get('longName', symbol),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'market_cap': info.get('marketCap', 0),
                'currency': info.get('currency', 'USD')
            }
        except:
            return {
                'name': symbol,
                'sector': 'Unknown',
                'industry': 'Unknown',
                'market_cap': 0,
                'currency': 'USD'
            }
    
    def validate_symbol(self, symbol: str) -> bool:
        """
        Validate if a stock symbol exists and has data.
        
        Args:
            symbol: Stock symbol to validate
            
        Returns:
            True if symbol is valid, False otherwise
        """
        try:
            ticker = yf.Ticker(symbol)
            # Try to get recent data (last 5 days)
            recent_data = ticker.history(period="5d")
            return not recent_data.empty
        except:
            return False
    
    def get_popular_stocks(self) -> dict:
        """
        Get a comprehensive list of popular stocks with company names.
        
        Returns:
            Dictionary mapping company names to stock symbols
        """
        return {
            # US Stocks
            'Apple Inc.': 'AAPL',
            'Microsoft Corporation': 'MSFT',
            'Alphabet Inc.': 'GOOGL',
            'Amazon.com Inc.': 'AMZN',
            'Tesla Inc.': 'TSLA',
            'Meta Platforms Inc.': 'META',
            'NVIDIA Corporation': 'NVDA',
            'JPMorgan Chase & Co.': 'JPM',
            'Johnson & Johnson': 'JNJ',
            'Visa Inc.': 'V',
            'Procter & Gamble Co.': 'PG',
            'UnitedHealth Group Inc.': 'UNH',
            'Home Depot Inc.': 'HD',
            'Mastercard Inc.': 'MA',
            'Walt Disney Co.': 'DIS',
            'PayPal Holdings Inc.': 'PYPL',
            'Bank of America Corp.': 'BAC',
            'Netflix Inc.': 'NFLX',
            'Adobe Inc.': 'ADBE',
            'Salesforce Inc.': 'CRM',
            'Comcast Corporation': 'CMCSA',
            'Exxon Mobil Corporation': 'XOM',
            'Verizon Communications Inc.': 'VZ',
            'Coca-Cola Co.': 'KO',
            'Abbott Laboratories': 'ABT',
            'Pfizer Inc.': 'PFE',
            'Thermo Fisher Scientific Inc.': 'TMO',
            'Costco Wholesale Corporation': 'COST',
            'Intel Corporation': 'INTC',
            'Cisco Systems Inc.': 'CSCO',
            'PepsiCo Inc.': 'PEP',
            'Oracle Corporation': 'ORCL',
            'IBM Corporation': 'IBM',
            'General Electric Co.': 'GE',
            'Ford Motor Co.': 'F',
            'General Motors Co.': 'GM',
            
            # Indian Stocks
            'Reliance Industries Ltd.': 'RELIANCE.NS',
            'Tata Consultancy Services Ltd.': 'TCS.NS',
            'HDFC Bank Ltd.': 'HDFCBANK.NS',
            'Infosys Ltd.': 'INFY.NS',
            'Hindustan Unilever Ltd.': 'HINDUNILVR.NS',
            'ICICI Bank Ltd.': 'ICICIBANK.NS',
            'State Bank of India': 'SBIN.NS',
            'Bharti Airtel Ltd.': 'BHARTIARTL.NS',
            'ITC Ltd.': 'ITC.NS',
            'Kotak Mahindra Bank Ltd.': 'KOTAKBANK.NS',
            'Asian Paints Ltd.': 'ASIANPAINT.NS',
            'Larsen & Toubro Ltd.': 'LT.NS',
            'Axis Bank Ltd.': 'AXISBANK.NS',
            'Maruti Suzuki India Ltd.': 'MARUTI.NS',
            'Sun Pharmaceutical Industries Ltd.': 'SUNPHARMA.NS',
            'Wipro Ltd.': 'WIPRO.NS',
            'HCL Technologies Ltd.': 'HCLTECH.NS',
            'Bajaj Finance Ltd.': 'BAJFINANCE.NS',
            'Titan Company Ltd.': 'TITAN.NS',
            'Mahindra & Mahindra Ltd.': 'M&M.NS',
            
            # European Stocks
            'ASML Holding N.V.': 'ASML',
            'LVMH Moët Hennessy Louis Vuitton': 'MC.PA',
            'Nestlé S.A.': 'NESN.SW',
            'SAP SE': 'SAP',
            'Roche Holding AG': 'ROG.SW',
            'Novartis AG': 'NOVN.SW',
            'Royal Dutch Shell plc': 'SHEL.L',
            'Unilever plc': 'ULVR.L',
            'AstraZeneca plc': 'AZN.L',
            'British Petroleum plc': 'BP.L',
            
            # Asian Stocks
            'Taiwan Semiconductor Manufacturing': 'TSM',
            'Alibaba Group Holding Ltd.': 'BABA',
            'Tencent Holdings Ltd.': '0700.HK',
            'Samsung Electronics Co. Ltd.': '005930.KS',
            'Toyota Motor Corporation': 'TM',
            'Sony Group Corporation': 'SONY',
        }
    
    def search_stocks(self, query: str) -> list:
        """
        Search for stocks by company name or symbol with intelligent matching.
        
        Args:
            query: Search query (company name or symbol)
            
        Returns:
            List of tuples (company_name, symbol) matching the query
        """
        stocks = self.get_popular_stocks()
        query_lower = query.lower().strip()
        results = []
        
        # If query is too short, return empty
        if len(query_lower) < 2:
            return results
        
        for company_name, symbol in stocks.items():
            company_lower = company_name.lower()
            symbol_lower = symbol.lower()
            
            score = 0
            # Exact symbol match (highest priority)
            if query_lower == symbol_lower or query_lower == symbol_lower.split('.')[0]:
                score = 100
            # Symbol starts with query
            elif symbol_lower.startswith(query_lower):
                score = 90
            # Company name starts with query
            elif company_lower.startswith(query_lower):
                score = 80
            # Symbol contains query
            elif query_lower in symbol_lower:
                score = 70
            # Company name contains query (exact word match)
            elif any(word.startswith(query_lower) for word in company_lower.split()):
                score = 60
            # Company name contains query (substring)
            elif query_lower in company_lower:
                score = 50
            # Fuzzy matching for common abbreviations
            elif self._fuzzy_match(query_lower, company_lower, symbol_lower):
                score = 40
            
            if score > 0:
                results.append((company_name, symbol, score))
        
        # Sort by score (descending) then by company name length
        results.sort(key=lambda x: (-x[2], len(x[0])))
        
        # Return tuples without score
        return [(name, symbol) for name, symbol, score in results[:12]]
    
    def _fuzzy_match(self, query: str, company: str, symbol: str) -> bool:
        """
        Fuzzy matching for common search patterns.
        """
        # Common abbreviations and alternative names
        abbreviations = {
            'apple': ['aapl', 'apple inc'],
            'microsoft': ['msft', 'microsoft corp'],
            'google': ['googl', 'alphabet'],
            'amazon': ['amzn', 'amazon.com'],
            'tesla': ['tsla', 'tesla inc'],
            'meta': ['meta', 'facebook'],
            'nvidia': ['nvda', 'nvidia corp'],
            'reliance': ['reliance.ns', 'reliance industries'],
            'tcs': ['tcs.ns', 'tata consultancy'],
            'infosys': ['infy.ns', 'infosys ltd'],
        }
        
        query_words = query.split()
        for word in query_words:
            if word in abbreviations:
                for abbrev in abbreviations[word]:
                    if abbrev in company.lower() or abbrev in symbol.lower():
                        return True
        
        return False
    
    def get_benchmark_data(self, benchmark: str, start_date: date, end_date: date) -> pd.DataFrame:
        """
        Get benchmark index data.
        
        Args:
            benchmark: Benchmark symbol
            start_date: Start date
            end_date: End date
            
        Returns:
            DataFrame with benchmark data
        """
        return self.get_stock_data(benchmark, start_date, end_date)
    
    def calculate_correlation(self, data1: pd.DataFrame, data2: pd.DataFrame) -> float:
        """
        Calculate correlation between two price series.
        
        Args:
            data1: First stock data
            data2: Second stock data
            
        Returns:
            Correlation coefficient
        """
        try:
            # Align data by index
            stock1_series = data1['Close'].copy()
            stock1_series.name = 'stock1'
            stock2_series = data2['Close'].copy()
            stock2_series.name = 'stock2'
            aligned_data = pd.concat([stock1_series, stock2_series], axis=1).dropna()
            
            if len(aligned_data) < 2:
                return 0.0
            
            # Calculate returns correlation
            returns1 = aligned_data['stock1'].pct_change().dropna()
            returns2 = aligned_data['stock2'].pct_change().dropna()
            
            correlation = returns1.corr(returns2)
            return correlation if not np.isnan(correlation) else 0.0
            
        except:
            return 0.0
