import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, date
import warnings
warnings.filterwarnings('ignore')

from strategies import MomentumStrategy, ValueStrategy, KeyMetricsCalculator
from data_fetcher import DataFetcher
from yfinance_search import YFinanceStockSearch
from autocomplete_components import stock_autocomplete, benchmark_autocomplete

def main():
    st.set_page_config(
        page_title="Momentum vs Value Investing Strategy Comparison",
        page_icon="📈",
        layout="wide"
    )
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "📖 Navigation",
        ["📈 Strategy Analysis", "🔬 Methodology"],
        index=0
    )
    
    if page == "🔬 Methodology":
        display_methodology()
        return
    
    # Light banner + global styles (force text -> black)
    st.markdown('''
<div style="
    background: linear-gradient(135deg, #f7f7f7 0%, #ffffff 100%);
    padding: 2rem;
    border-radius: 8px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    border: 1px solid #e8e8e8;
">
    <h1 style="color: #000000; font-size: 2.5rem; margin: 0; font-weight: 600;">
        📈 Momentum vs Value Strategy Analysis
    </h1>
    <p style="color: #000000; font-size: 1.1rem; margin: 0.5rem 0 0 0; font-weight: 400;">
        Compare investment strategies with 60+ global benchmarks and thousands of worldwide stocks
    </p>
</div>

<style>
/* -------- Global: make ALL app text black -------- */
:root { --text-color:#000000; --text-color-rgb:0,0,0; }

body, [data-testid="stAppViewContainer"] * ,
[data-testid="stSidebar"] * ,
[data-testid="stMarkdownContainer"] * ,
h1, h2, h3, h4, h5, h6,
p, li, span, label, small, div {
  color:#000000 !important;
}

/* Metrics, sliders, and helper labels */
[data-testid="stMetricLabel"],
[data-testid="stMetricValue"],
[data-testid="stSlider"] label,
[data-testid="stTickBarMin"],
[data-testid="stTickBarMax"],
[data-testid="stMarkdown"] {
  color:#000000 !important;
}

/* Expander content */
[data-testid="stExpander"] * { color:#000000 !important; }

/* Container backgrounds */
.main > div { background-color:#ffffff; color:#000000; }
.stApp { background-color:#ffffff; }

/* Buttons */
.stButton > button {
  background: #ffffff ;
  color: #000000 ;
  border: 1px solid #e0e0e0 ;
  border-radius: 6px ;
  padding: 0.6rem 1.2rem ;
  font-weight: 500 ;
  transition: all 0.2s ease ;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1) ;
}
.stButton > button:hover {
  background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
  transform: translateY(-1px);
  box-shadow:0 2px 6px rgba(0,0,0,.15);
}

/* Inputs */
.stTextInput > div > div > input {
  border-radius:6px; border:1px solid #e0e0e0; background-color:#ffffff;
  color:#000000; transition:all .2s ease;
}
.stTextInput > div > div > input:focus {
  border-color:#666666; box-shadow:0 0 0 .1rem rgba(102,102,102,.2);
}

/* Selects */
.stSelectbox > div > div {
  border-radius:6px; border:1px solid #e0e0e0; background-color:#ffffff;
  color:#000000;
}

/* Headings */
h1, h2, h3, h4 { color:#000000; font-weight:600; }
/* Autocomplete suggestions dropdown */
div[data-baseweb="popover"] {
  background-color: #ffffff !important; /* white background */
  border: 1px solid #dcdcdc !important;
  border-radius: 6px !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
  color: #000000 !important; /* black text */
}

/* Make the "Suggestions" header white with black text */
div[data-baseweb="popover"] [data-testid="stMarkdownContainer"] {
  background-color: #ffffff !important;
  color: #000000 !important;
}

/* Make each suggestion white with black text */
div[data-baseweb="popover"] [role="option"] {
  background-color: #ffffff !important;
  color: #000000 !important;
}

/* Hover effect for suggestions */
div[data-baseweb="popover"] [role="option"]:hover {
  background-color: #f2f2f2 !important;
  color: #000000 !important;
}

</style>
''', unsafe_allow_html=True)

    
    # Main content area - unified layout
    st.markdown('<h2 style="color: #000000; text-align: center; margin: 2rem 0;">🎛️ Strategy Configuration</h2>', unsafe_allow_html=True)
    
    # Initialize data fetcher and search
    data_fetcher_instance = DataFetcher()
    yfinance_search = YFinanceStockSearch()
    
    # Create main configuration columns
    config_col1, config_col2 = st.columns([1, 1])
    
    with config_col1:
        # Benchmark autocomplete
        benchmark_selection = benchmark_autocomplete(
            "📈 Benchmark Selection",
            "🔍 Type 'S&P', 'Nifty', 'FTSE', 'DAX'...",
            "benchmark",
            yfinance_search,
            "Search from 60+ global indices, commodities, and crypto"
        )
        
        if benchmark_selection:
            benchmark_name, benchmark_symbol = benchmark_selection
        else:
            benchmark_symbol = "^GSPC"  # Default to S&P 500
            benchmark_name = "S&P 500"
    
    with config_col2:
        st.markdown('<h4 style="color: #000000;">📅 Date Range</h4>', unsafe_allow_html=True)
        start_date = st.date_input(
            "Start Date",
            value=date(2015, 1, 1),
            min_value=date(2010, 1, 1),
            max_value=date(2025, 12, 31),
            label_visibility="collapsed"
        )
        end_date = st.date_input(
            "End Date", 
            value=date(2024, 12, 31),
            min_value=date(2010, 1, 1),
            max_value=date(2025, 12, 31),
            label_visibility="collapsed"
        )
        
    # Stock selection section
    st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)  # Spacer
    st.markdown('<h2 style="color: #000000; text-align: center; margin: 2rem 0;">🎯 Stock Selection</h2>', unsafe_allow_html=True)
    
    # Initialize variables to avoid scoping issues
    selected_stock_symbols = []
    stock1_symbol = 'AAPL'
    stock1_name = 'Apple Inc.'
    stock2_symbol = benchmark_symbol
    stock2_name = benchmark_name
    
    # Multiple stock selection for benchmark comparison
    st.markdown('<h3 style="color: #000000; margin-bottom: 1.5rem;">🎯 Select Multiple Stocks for Benchmark Comparison</h3>', unsafe_allow_html=True)
    
    # Initialize selected stocks list
    if 'selected_stocks' not in st.session_state:
        st.session_state.selected_stocks = []
    
    # Stock autocomplete for adding to multi-select
    stock_selection = stock_autocomplete(
        "🔍 Add Stocks to Comparison",
        "🔍 Type 'Apple', 'Tesla', 'Microsoft'...",
        "multi_stock",
        yfinance_search,
        "Search thousands of stocks worldwide"
    )
    
    # Add selected stock to list
    if stock_selection:
        company, symbol = stock_selection
        if symbol not in [s['symbol'] for s in st.session_state.selected_stocks]:
            stock_info = yfinance_search.get_stock_info_yfinance(symbol)
            st.session_state.selected_stocks.append({
                'symbol': symbol,
                'name': company,
                'market': stock_info['market']
            })
            # Clear the selection to allow adding more
            st.session_state.multi_stock_selected = None
            st.session_state.multi_stock_query = ""
            st.rerun()
    
    # Display selected stocks
    if st.session_state.selected_stocks:
        st.markdown('<h4 style="color: #000000; margin-top: 2rem;">📊 Selected Stocks for Comparison</h4>', unsafe_allow_html=True)
        
        for i, stock in enumerate(st.session_state.selected_stocks):
            col1, col2 = st.columns([4, 1])
            with col1:
                market_emoji = "🇺🇸" if "US" in stock['market'] else "🇮🇳" if "India" in stock['market'] else "🇬🇧" if "UK" in stock['market'] else "🇯🇵" if "Japan" in stock['market'] else "🌍"
                st.markdown(
                    f'<div style="background: #f8f8f8; padding: 0.5rem; border-radius: 6px; color: #000000; margin: 0.2rem 0; border: 1px solid #e0e0e0;">{market_emoji} <strong>{stock["name"]} ({stock["symbol"]})</strong> • {stock["market"]}</div>',
                    unsafe_allow_html=True
                )
            with col2:
                if st.button("🗑️", key=f"remove_{stock['symbol']}", help="Remove stock"):
                    st.session_state.selected_stocks.pop(i)
                    st.rerun()
    
    else:
        st.markdown('<div style="background: #f5f5f5; padding: 1rem; border-radius: 6px; color: #000000; text-align: center; margin: 1rem 0; border: 1px solid #e0e0e0;">📋 No stocks selected yet. Search and click ➕ to add stocks for comparison.</div>', unsafe_allow_html=True)
    
    # For multi-stock analysis, use all selected stocks
    if st.session_state.selected_stocks:
        stock1_symbol = st.session_state.selected_stocks[0]['symbol']
        selected_stock_symbols = [stock['symbol'] for stock in st.session_state.selected_stocks]
    else:
        stock1_symbol = 'AAPL'
        selected_stock_symbols = ['AAPL']
    stock2_symbol = benchmark_symbol
    stock2_name = benchmark_name
        
    # Strategy parameters section
    st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)  # Spacer
    st.markdown('<h2 style="color: #000000; text-align: center; margin: 2rem 0;">⚙️ Strategy Parameters</h2>', unsafe_allow_html=True)
    
    param_col1, param_col2 = st.columns(2)
    with param_col1:
        st.markdown('<h4 style="color: #000000;">📊 Momentum Strategy</h4>', unsafe_allow_html=True)
        momentum_period = st.slider("Lookback Period (days)", 30, 500, 120, key="momentum")
    
    with param_col2:
        st.markdown('<h4 style="color: #000000;">💰 Value Strategy</h4>', unsafe_allow_html=True)
        value_period = st.slider("Analysis Period (days)", 120, 1000, 365, key="value")
    
    # Run strategy button
    st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)  # Spacer
    col_center = st.columns([1, 2, 1])[1]
    with col_center:
        run_strategy = st.button("🚀 Run Strategy Analysis", type="primary", use_container_width=True)
    
    # Main content area
    if run_strategy and stock1_symbol:
        if not stock1_symbol:
            st.error("Please enter a valid stock symbol")
            return
            
        if not st.session_state.selected_stocks:
            st.error("Please select at least one stock for benchmark comparison")
            return
            
        with st.spinner("Fetching data and running analysis..."):
            try:
                # Initialize data fetcher and strategies
                data_fetcher = DataFetcher()
                momentum_strategy = MomentumStrategy(momentum_period)
                value_strategy = ValueStrategy(value_period)
                
                # Multi-stock vs benchmark analysis
                display_multi_stock_results(
                    selected_stock_symbols, benchmark_symbol, benchmark_name,
                    data_fetcher, momentum_strategy, value_strategy, 
                    start_date, end_date
                )
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please check your stock symbols and internet connection.")
    
    else:
        # Display strategy explanations
        display_strategy_explanations()

def display_multi_stock_results(selected_symbols, benchmark_symbol, benchmark_name,
                               data_fetcher, momentum_strategy, value_strategy, 
                               start_date, end_date):
    """Display analysis results for multiple stocks vs benchmark"""
    
    st.markdown('<h2 style="color: #000000; text-align: center; margin: 2rem 0;">📊 Multi-Stock Analysis Results</h2>', unsafe_allow_html=True)
    
    if not selected_symbols:
        st.error("No stocks selected for analysis")
        return
    
    # Fetch benchmark data first
    benchmark_data = data_fetcher.get_stock_data(benchmark_symbol, start_date, end_date)
    if benchmark_data.empty:
        st.error(f"Failed to fetch benchmark data for {benchmark_name}")
        return
    
    # Calculate benchmark strategies
    benchmark_momentum = momentum_strategy.calculate(benchmark_data)
    benchmark_value = value_strategy.calculate(benchmark_data)
    
    # Store data for all stocks
    stocks_data = {}
    stocks_momentum = {}
    stocks_value = {}
    
    # Fetch data for all selected stocks
    for symbol in selected_symbols:
        stock_data = data_fetcher.get_stock_data(symbol, start_date, end_date)
        if not stock_data.empty:
            stocks_data[symbol] = stock_data
            stocks_momentum[symbol] = momentum_strategy.calculate(stock_data)
            stocks_value[symbol] = value_strategy.calculate(stock_data)
    
    if not stocks_data:
        st.error("Failed to fetch data for any selected stocks")
        return
    
    # Performance metrics section
    st.subheader("📊 Performance Overview")
    
    # Create metrics comparison table
    metrics_data = []
    for symbol in stocks_data.keys():
        stock_data = stocks_data[symbol]
        stock_return = ((stock_data['Close'].iloc[-1] / stock_data['Close'].iloc[0]) - 1) * 100
        
        momentum_signal = "📈 BUY" if not stocks_momentum[symbol].empty and stocks_momentum[symbol]['signal'].iloc[-1] > 0 else "📉 SELL"
        value_signal = "📈 BUY" if not stocks_value[symbol].empty and stocks_value[symbol]['signal'].iloc[-1] > 0 else "📉 SELL"
        
        metrics_data.append([symbol, f"{stock_return:.2f}%", momentum_signal, value_signal])
    
    # Add benchmark to metrics
    benchmark_return = ((benchmark_data['Close'].iloc[-1] / benchmark_data['Close'].iloc[0]) - 1) * 100
    benchmark_momentum_signal = "📈 BUY" if not benchmark_momentum.empty and benchmark_momentum['signal'].iloc[-1] > 0 else "📉 SELL"
    benchmark_value_signal = "📈 BUY" if not benchmark_value.empty and benchmark_value['signal'].iloc[-1] > 0 else "📉 SELL"
    metrics_data.append([f"{benchmark_name} (Benchmark)", f"{benchmark_return:.2f}%", benchmark_momentum_signal, benchmark_value_signal])
    
    # Display metrics table
    metrics_df = pd.DataFrame(metrics_data)
    metrics_df.columns = ["Asset", "Total Return", "Momentum Signal", "Value Signal"]
    st.dataframe(metrics_df, use_container_width=True)
    
    # Key Metrics Expanders for all assets
    st.subheader("📋 Key Metrics & Formulas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📈 Selected Stocks**")
        for symbol in stocks_data.keys():
            with st.expander(f"📊 {symbol} - Key Metrics & Formulas", expanded=False):
                metrics = KeyMetricsCalculator.calculate_comprehensive_metrics(stocks_data[symbol], symbol)
                if metrics and 'error' not in metrics:
                    for metric_name, metric_data in metrics.items():
                        st.markdown(f"**{metric_name}**")
                        st.markdown(f"*Formula*: {metric_data['formula']}")
                        st.markdown(f"*Calculation*: {metric_data['calculation']}")
                        st.markdown(f"*Value*: **{metric_data['value']}**")
                        st.markdown("---")
                else:
                    st.error(f"❌ Unable to calculate metrics for {symbol}")
    
    with col2:
        st.markdown("**📊 Benchmark**")
        with st.expander(f"📊 {benchmark_name} - Key Metrics & Formulas", expanded=False):
            benchmark_metrics = KeyMetricsCalculator.calculate_comprehensive_metrics(benchmark_data, benchmark_symbol)
            if benchmark_metrics and 'error' not in benchmark_metrics:
                for metric_name, metric_data in benchmark_metrics.items():
                    st.markdown(f"**{metric_name}**")
                    st.markdown(f"*Formula*: {metric_data['formula']}")
                    st.markdown(f"*Calculation*: {metric_data['calculation']}")
                    st.markdown(f"*Value*: **{metric_data['value']}**")
                    st.markdown("---")
            else:
                st.error(f"❌ Unable to calculate metrics for {benchmark_name}")
    
    # Charts section
    st.subheader("📈 Multi-Stock Comparison Charts")
    
    # Price comparison chart (normalized)
    fig_price = go.Figure()
    
    # Add benchmark first
    benchmark_normalized = (benchmark_data['Close'] / benchmark_data['Close'].iloc[0]) * 100
    fig_price.add_trace(go.Scatter(
        x=benchmark_data.index,
        y=benchmark_normalized,
        mode='lines',
        name=f"{benchmark_name} (Benchmark)",
        line=dict(color='black', width=3, dash='dash')
    ))
    
    # Add all selected stocks
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    for i, symbol in enumerate(stocks_data.keys()):
        stock_data = stocks_data[symbol]
        stock_normalized = (stock_data['Close'] / stock_data['Close'].iloc[0]) * 100
        
        fig_price.add_trace(go.Scatter(
            x=stock_data.index,
            y=stock_normalized,
            mode='lines',
            name=f"{symbol}",
            line=dict(color=colors[i % len(colors)], width=2)
        ))
    
    fig_price.update_layout(
        title="Normalized Price Comparison vs Benchmark (Base = 100)",
        xaxis_title="Date",
        yaxis_title="Normalized Price",
        hovermode='x unified',
        height=500,
        font=dict(color="#000000"),
        title_font=dict(color="#000000")
    )
    
    st.plotly_chart(fig_price, use_container_width=True)
    
    # Strategy performance comparison
    if len(selected_symbols) <= 4:  # Only show strategy charts for manageable number of stocks
        fig_strategies = make_subplots(
            rows=2, cols=len(selected_symbols),
            subplot_titles=[f"{symbol} Momentum" for symbol in selected_symbols] + 
                          [f"{symbol} Value" for symbol in selected_symbols],
            vertical_spacing=0.15
        )
        
        for i, symbol in enumerate(selected_symbols):
            if not stocks_momentum[symbol].empty:
                fig_strategies.add_trace(
                    go.Scatter(x=stocks_momentum[symbol].index, 
                             y=stocks_momentum[symbol]['cumulative_return'],
                             mode='lines', name=f"{symbol} Momentum", 
                             line=dict(color=colors[i % len(colors)])),
                    row=1, col=i+1
                )
            
            if not stocks_value[symbol].empty:
                fig_strategies.add_trace(
                    go.Scatter(x=stocks_value[symbol].index, 
                             y=stocks_value[symbol]['cumulative_return'],
                             mode='lines', name=f"{symbol} Value", 
                             line=dict(color=colors[i % len(colors)])),
                    row=2, col=i+1
                )
        
        fig_strategies.update_layout(
            title="Individual Stock Strategy Performance",
            height=600,
            showlegend=False,
            font=dict(color="#000000"),
            title_font=dict(color="#000000")
        )
        
        st.plotly_chart(fig_strategies, use_container_width=True)
    
    # Strategy performance summary
    st.subheader("🎯 Strategy Performance Summary")
    
    summary_data = []
    
    # Add benchmark strategies
    if not benchmark_momentum.empty:
        benchmark_mom_return = benchmark_momentum['cumulative_return'].iloc[-1] * 100
        summary_data.append([f"{benchmark_name} (Benchmark)", "Momentum", f"{benchmark_mom_return:.2f}%"])
    
    if not benchmark_value.empty:
        benchmark_val_return = benchmark_value['cumulative_return'].iloc[-1] * 100
        summary_data.append([f"{benchmark_name} (Benchmark)", "Value", f"{benchmark_val_return:.2f}%"])
    
    # Add stock strategies
    for symbol in selected_symbols:
        if not stocks_momentum[symbol].empty:
            mom_return = stocks_momentum[symbol]['cumulative_return'].iloc[-1] * 100
            summary_data.append([symbol, "Momentum", f"{mom_return:.2f}%"])
        
        if not stocks_value[symbol].empty:
            val_return = stocks_value[symbol]['cumulative_return'].iloc[-1] * 100
            summary_data.append([symbol, "Value", f"{val_return:.2f}%"])
    
    if summary_data:
        summary_df = pd.DataFrame(summary_data)
        summary_df.columns = ["Asset", "Strategy", "Total Return"]
        st.dataframe(summary_df, use_container_width=True)

def display_results(stock1_symbol, stock2_name, stock2_symbol, stock1_data, stock2_data, 
                   stock1_momentum, stock1_value, stock2_momentum, stock2_value):
    """Display analysis results with charts and metrics"""
    
    # Performance metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"{stock1_symbol} Performance")
        stock1_return = ((stock1_data['Close'].iloc[-1] / stock1_data['Close'].iloc[0]) - 1) * 100
        st.metric("Total Return", f"{stock1_return:.2f}%")
        
        if not stock1_momentum.empty:
            momentum_signal = "📈 BUY" if stock1_momentum['signal'].iloc[-1] > 0 else "📉 SELL"
            st.metric("Momentum Signal", momentum_signal)
        
        if not stock1_value.empty:
            value_signal = "📈 BUY" if stock1_value['signal'].iloc[-1] > 0 else "📉 SELL"
            st.metric("Value Signal", value_signal)
        
        # Key Metrics Expander for Stock 1
        with st.expander(f"📊 Key Metrics & Formulas - {stock1_symbol}", expanded=False):
            metrics1 = KeyMetricsCalculator.calculate_comprehensive_metrics(stock1_data, stock1_symbol)
            if metrics1 and 'error' not in metrics1:
                for metric_name, metric_data in metrics1.items():
                    st.markdown(f"**{metric_name}**")
                    st.markdown(f"*Formula*: {metric_data['formula']}")
                    st.markdown(f"*Calculation*: {metric_data['calculation']}")
                    st.markdown(f"*Value*: **{metric_data['value']}**")
                    st.markdown("---")
            else:
                st.error(f"❌ Unable to calculate metrics for {stock1_symbol}")
    
    with col2:
        st.subheader(f"{stock2_name} Performance")
        stock2_return = ((stock2_data['Close'].iloc[-1] / stock2_data['Close'].iloc[0]) - 1) * 100
        st.metric("Total Return", f"{stock2_return:.2f}%")
        
        if not stock2_momentum.empty:
            momentum_signal = "📈 BUY" if stock2_momentum['signal'].iloc[-1] > 0 else "📉 SELL"
            st.metric("Momentum Signal", momentum_signal)
        
        if not stock2_value.empty:
            value_signal = "📈 BUY" if stock2_value['signal'].iloc[-1] > 0 else "📉 SELL"
            st.metric("Value Signal", value_signal)
        
        # Key Metrics Expander for Stock 2 / Benchmark
        with st.expander(f"📊 Key Metrics & Formulas - {stock2_name}", expanded=False):
            metrics2 = KeyMetricsCalculator.calculate_comprehensive_metrics(stock2_data, stock2_symbol)
            if metrics2 and 'error' not in metrics2:
                for metric_name, metric_data in metrics2.items():
                    st.markdown(f"**{metric_name}**")
                    st.markdown(f"*Formula*: {metric_data['formula']}")
                    st.markdown(f"*Calculation*: {metric_data['calculation']}")
                    st.markdown(f"*Value*: **{metric_data['value']}**")
                    st.markdown("---")
            else:
                st.error(f"❌ Unable to calculate metrics for {stock2_name}")
    
    # Charts
    st.subheader("Strategy Comparison Charts")
    
    # Price comparison chart
    fig_price = go.Figure()
    
    # Normalize prices to 100 for comparison
    stock1_normalized = (stock1_data['Close'] / stock1_data['Close'].iloc[0]) * 100
    stock2_normalized = (stock2_data['Close'] / stock2_data['Close'].iloc[0]) * 100
    
    fig_price.add_trace(go.Scatter(
        x=stock1_data.index,
        y=stock1_normalized,
        mode='lines',
        name=f"{stock1_symbol} Price",
        line=dict(color='blue', width=2)
    ))
    
    fig_price.add_trace(go.Scatter(
        x=stock2_data.index,
        y=stock2_normalized,
        mode='lines',
        name=f"{stock2_name} Price",
        line=dict(color='red', width=2)
    ))
    
    fig_price.update_layout(
        title="Normalized Price Comparison (Base = 100)",
        xaxis_title="Date",
        yaxis_title="Normalized Price",
        hovermode='x unified',
        font=dict(color="#000000"),
        title_font=dict(color="#000000")
    )
    
    st.plotly_chart(fig_price, use_container_width=True)
    
    # Strategy signals chart
    if not stock1_momentum.empty and not stock1_value.empty:
        fig_signals = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                f"{stock1_symbol} Momentum Strategy",
                f"{stock1_symbol} Value Strategy",
                f"{stock2_name} Momentum Strategy",
                f"{stock2_name} Value Strategy"
            ),
            vertical_spacing=0.1
        )
        
        # Stock 1 Momentum
        fig_signals.add_trace(
            go.Scatter(x=stock1_momentum.index, y=stock1_momentum['cumulative_return'],
                      mode='lines', name=f"{stock1_symbol} Momentum", line=dict(color='green')),
            row=1, col=1
        )
        
        # Stock 1 Value
        fig_signals.add_trace(
            go.Scatter(x=stock1_value.index, y=stock1_value['cumulative_return'],
                      mode='lines', name=f"{stock1_symbol} Value", line=dict(color='blue')),
            row=1, col=2
        )
        
        # Stock 2 Momentum
        if not stock2_momentum.empty:
            fig_signals.add_trace(
                go.Scatter(x=stock2_momentum.index, y=stock2_momentum['cumulative_return'],
                          mode='lines', name=f"{stock2_name} Momentum", line=dict(color='orange')),
                row=2, col=1
            )
        
        # Stock 2 Value
        if not stock2_value.empty:
            fig_signals.add_trace(
                go.Scatter(x=stock2_value.index, y=stock2_value['cumulative_return'],
                          mode='lines', name=f"{stock2_name} Value", line=dict(color='purple')),
                row=2, col=2
            )
        
        fig_signals.update_layout(
            title="Strategy Performance Comparison",
            height=600,
            showlegend=False,
            font=dict(color="#000000"),
            title_font=dict(color="#000000")
        )
        
        st.plotly_chart(fig_signals, use_container_width=True)
    
    # Strategy comparison table
    st.subheader("Strategy Performance Summary")
    
    summary_data = []
    
    if not stock1_momentum.empty:
        mom_return = stock1_momentum['cumulative_return'].iloc[-1] * 100
        summary_data.append([f"{stock1_symbol}", "Momentum", f"{mom_return:.2f}%"])
    
    if not stock1_value.empty:
        val_return = stock1_value['cumulative_return'].iloc[-1] * 100
        summary_data.append([f"{stock1_symbol}", "Value", f"{val_return:.2f}%"])
    
    if not stock2_momentum.empty:
        mom_return = stock2_momentum['cumulative_return'].iloc[-1] * 100
        summary_data.append([f"{stock2_name}", "Momentum", f"{mom_return:.2f}%"])
    
    if not stock2_value.empty:
        val_return = stock2_value['cumulative_return'].iloc[-1] * 100
        summary_data.append([f"{stock2_name}", "Value", f"{val_return:.2f}%"])
    
    if summary_data:
        summary_df = pd.DataFrame(summary_data)
        summary_df.columns = ["Asset", "Strategy", "Total Return"]
        st.dataframe(summary_df, use_container_width=True)

def display_methodology():
    """Display methodology page with key metrics definitions"""
    
    # Light banner for methodology (text -> black)
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f7f7f7 0%, #ffffff 100%);
        padding: 2rem;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        border: 1px solid #e8e8e8;
    ">
        <h1 style="color: #000000; font-size: 2.5rem; margin: 0; font-weight: 600;">
            🔬 Methodology & Key Metrics
        </h1>
        <p style="color: #000000; font-size: 1.1rem; margin: 0.5rem 0 0 0; font-weight: 400;">
            Understanding the financial metrics and formulas used in our analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## 📊 Key Financial Metrics")
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 💰 Price & Return Metrics
        
        **Average Price**
        - *Formula*: (Opening Price on first day + Closing Price on last day) ÷ 2
        - *Purpose*: Simple average of start and end prices over the analysis period
        - *Interpretation*: Gives a baseline price reference for the investment period
        
        **Cumulative Return**
        - *Formula*: (Final Price ÷ Initial Price) - 1
        - *Purpose*: Total return over the entire analysis period
        - *Interpretation*: Positive values indicate gains, negative values indicate losses
        
        **Sharpe Ratio**
        - *Formula*: (Mean(Returns) ÷ Std(Returns)) × √252
        - *Purpose*: Risk-adjusted return measure
        - *Interpretation*: Higher values indicate better risk-adjusted performance
        - *Note*: √252 annualizes the ratio (252 trading days per year)
        
        **Max Drawdown**
        - *Formula*: (Trough Value – Peak Value) ÷ Peak Value
        - *Purpose*: Largest peak-to-trough decline
        - *Interpretation*: Measures the worst-case loss from any peak
        """)
    
    with col2:
        st.markdown("""
        ### 📈 Valuation Metrics
        
        **P/E Ratio (Price-to-Earnings)**
        - *Formula*: Price ÷ Earnings per Share
        - *Purpose*: Valuation metric comparing price to earnings
        - *Interpretation*: Lower ratios may indicate undervaluation
        - *Data Source*: Real-time data from Yahoo Finance
        
        **P/B Ratio (Price-to-Book)**
        - *Formula*: Price ÷ Book Value per Share
        - *Purpose*: Compares market value to book value
        - *Interpretation*: Values below 1 may indicate undervaluation
        - *Data Source*: Real-time data from Yahoo Finance
        
        **Dividend Yield**
        - *Formula*: Annual Dividends ÷ Price × 100%
        - *Purpose*: Income return from dividends
        - *Interpretation*: Higher yields provide more income
        - *Data Source*: Real-time data from Yahoo Finance
        """)
    
    st.markdown("---")
    
    st.markdown("## 🎯 Investment Strategies")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        ### 📈 Momentum Strategy
        
        **Core Principle**: "The trend is your friend"
        
        **Implementation**:
        - Calculates rolling returns over 60-day periods
        - Compares current price to moving average
        - Generates buy signals when momentum is positive
        - Generates sell signals when momentum turns negative
        
        **Key Indicators**:
        - Rolling return > 0 AND price > 102% of moving average → BUY
        - Rolling return < 0 OR price < 98% of moving average → SELL
        
        **Best For**: Trending markets, growth stocks
        """)
    
    with col4:
        st.markdown("""
        ### 💰 Value Strategy
        
        **Core Principle**: "Buy low, sell high"
        
        **Implementation**:
        - Analyzes price relative to long-term average (252 days)
        - Uses RSI to identify oversold/overbought conditions
        - Contrarian approach - buys when others sell
        
        **Key Indicators**:
        - Price < 95% of long-term average AND RSI < 30 → BUY
        - Price > 105% of long-term average AND RSI > 70 → SELL
        
        **Best For**: Market corrections, undervalued stocks
        """)
    
    st.markdown("---")
    
    st.markdown("""
    ## 📝 Data Sources & Methodology
    
    **Real-time Data**: All price data and fundamental metrics are sourced from Yahoo Finance API
    
    **Calculation Period**: Metrics are calculated over the selected date range in the analysis
    
    **Global Coverage**: Supports stocks and indices from major exchanges worldwide including:
    - 🇺🇸 US: NYSE, NASDAQ (S&P 500, Apple, Microsoft, etc.)
    - 🇮🇳 India: NSE, BSE (Nifty 50, Reliance, TCS, etc.)
    - 🇪🇺 Europe: London, Frankfurt, Paris (FTSE 100, DAX, CAC 40, etc.)
    - 🌏 Asia: Tokyo, Hong Kong, Shanghai (Nikkei, Hang Seng, etc.)
    
    **Strategy Signals**: All buy/sell signals are calculated using the historical data within your selected timeframe
    
    **Risk Disclaimer**: This tool is for educational and analysis purposes only. Past performance does not guarantee future results.
    """)

def display_strategy_explanations():
    """Display strategy explanations when no analysis is running"""
    
    st.markdown("## Strategy Explanations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📈 Momentum Strategy
        
        **Concept**: Buy assets that are trending upward and sell those trending downward.
        
        **Implementation**:
        - Calculate rolling returns over specified period
        - Generate buy signals when momentum is positive
        - Generate sell signals when momentum turns negative
        - Track cumulative returns from strategy signals
        
        **Key Principle**: "The trend is your friend" - assets that have been rising tend to continue rising in the short term.
        """)
    
    with col2:
        st.markdown("""
        ### 💰 Value Strategy
        
        **Concept**: Buy undervalued assets and sell overvalued ones based on fundamental metrics.
        
        **Implementation**:
        - Analyze price-to-moving-average ratios
        - Calculate relative strength indicators
        - Generate buy signals when assets appear undervalued
        - Generate sell signals when assets appear overvalued
        
        **Key Principle**: "Buy low, sell high" - assets trading below their intrinsic value will eventually revert to fair value.
        """)
    
    st.markdown("""
    ## How to Use This Tool
    
    1. **Select a benchmark** from the dropdown (S&P 500, Nifty 50, etc.)
    2. **Choose comparison type** - compare a stock against the benchmark or compare two stocks
    3. **Find stocks easily**:
       - Use quick-select buttons for popular stocks (Apple, Tesla, Google, etc.)
       - Search by company name (e.g., "Apple", "Tesla", "Microsoft")
       - Enter stock symbols directly (e.g., AAPL, TSLA, RELIANCE.NS)
       - Get suggestions as you type company names
    4. **Set date range** for your analysis period
    5. **Adjust strategy parameters** if desired
    6. **Click "Run Strategy Analysis"** to see results
    
    **Global Stock Search Features:**
    - Search thousands of stocks worldwide by company name or symbol
    - Type "Apple", "Samsung", "Toyota", "Reliance" to find companies instantly
    - Search by sector: "bank", "tech", "pharma", "auto" to discover related companies
    - Covers major exchanges: US (NASDAQ/NYSE), India (NSE), UK (LSE), Japan (TSE), Canada (TSX), Australia (ASX), and more
    - Live results with country flags and market information
    - Clean, animated interface with chromatic colors
    
    **Global Benchmark Coverage (60+ Indices):**
    - **US**: S&P 500, NASDAQ, Dow Jones, Russell 2000, and more
    - **India**: Nifty 50, Sensex, Nifty Midcap, Nifty Bank, Nifty IT, sector indices
    - **Europe**: FTSE 100, DAX, CAC 40, Euro Stoxx 50, and all major European indices
    - **Asia**: Nikkei, Hang Seng, Shanghai, KOSPI, ASX 200, and more
    - **Americas**: TSX (Canada), Bovespa (Brazil), IPC (Mexico), and more
    - **Commodities**: Gold, Oil, Bitcoin, Ethereum, and major commodities
    
    The tool will display performance metrics, interactive charts, and strategy signals to help you understand how momentum and value strategies perform across different assets and time periods worldwide.
    """)

if __name__ == "__main__":
    main()
