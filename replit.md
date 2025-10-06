# Momentum vs Value Investing Strategy Comparison

## Overview

This is a Streamlit-based financial analysis application that compares momentum and value investing strategies using real market data from global exchanges. The application features a dynamic real-time stock search system powered by yfinance that provides access to thousands of companies from major world markets including US (NASDAQ/NYSE), India (NSE), UK (LSE), Japan (TSE), Canada (TSX), Australia (ASX), Germany (XETRA), and more. Users can search by company name, sector keywords, or symbols with intelligent live suggestions powered by Yahoo Finance's search API. It fetches real stock data through Yahoo Finance, implements two distinct investment strategies (momentum and value), and provides interactive visualizations to analyze their performance against various market benchmarks.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

**Frontend Architecture**: Built using Streamlit as a single-page web application with sidebar controls and main content area. Features a real-time global stock search system powered by yfinance with live suggestions from Yahoo Finance's comprehensive database, company name lookup, symbol validation, market identification with country flags, and dynamic stock recommendations. The interface uses Plotly for interactive charting and visualization, providing real-time strategy comparison charts and performance metrics.

**Data Processing Layer**: Implements a modular strategy pattern with separate classes for MomentumStrategy and ValueStrategy. Each strategy class contains its own calculation logic and signal generation methods, making it easy to add new strategies or modify existing ones.

**Data Management**: Uses a DataFetcher class that implements caching to optimize API calls to Yahoo Finance. The caching mechanism prevents redundant data requests and improves application performance during repeated analysis.

**Strategy Implementation**: 
- MomentumStrategy: Based on rolling returns and trend analysis with configurable lookback periods
- ValueStrategy: (Implementation not visible in provided files but follows similar pattern)
- Both strategies generate buy/sell signals and calculate cumulative returns for performance comparison

**Configuration Management**: Supports 60+ global market benchmarks including all major stock indices (S&P 500, Nifty 50, Sensex, NASDAQ, FTSE 100, DAX, Nikkei 225, Hang Seng, etc.), sector-specific indices (Nifty Bank, Nifty IT, etc.), regional indices from Americas/Europe/Asia/Middle East/Africa, and commodities/cryptocurrencies (Gold, Oil, Bitcoin) with flexible comparison types configurable through the sidebar interface.

## External Dependencies

**Data Provider**: Yahoo Finance API accessed through the yfinance Python library for real-time and historical stock market data across global exchanges.

**Visualization Libraries**: 
- Plotly for interactive financial charts and subplots
- Streamlit for web application framework and UI components

**Data Processing**: 
- Pandas for data manipulation and time series analysis
- NumPy for numerical computations and array operations

**Market Data Sources**: Supports data from major global exchanges including US markets (NYSE, NASDAQ), Indian markets (NSE), European markets (FTSE, DAX), and Asian markets (Nikkei, Hang Seng, Shanghai Composite).

**Python Dependencies**: Built on Python with core libraries for financial analysis, data visualization, and web application development.