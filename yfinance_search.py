import yfinance as yf
import pandas as pd
from typing import List, Tuple, Dict, Optional
import streamlit as st

class YFinanceStockSearch:
    """
    Dynamic stock search using yfinance for real-time stock recommendations
    """
    
    def __init__(self):
        self.search_cache = {}
        
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def search_stocks_autocomplete(_self, query: str, limit: int = 8) -> List[Tuple[str, str]]:
        """
        Search for stocks using yfinance Search functionality
        Returns list of tuples: (company_name, symbol)
        """
        try:
            if len(query) < 2:
                return []
                
            # Use yfinance Search to find stocks
            search = yf.Search(query)
            
            stock_results = []
            # Get quotes from search
            if hasattr(search, 'quotes') and search.quotes:
                for result in search.quotes[:limit]:
                    try:
                        symbol = result.get('symbol', '')
                        name = result.get('longname') or result.get('shortname') or result.get('name', symbol)
                        
                        # Skip if no name or symbol
                        if not symbol or not name:
                            continue
                            
                        # Clean up the name and symbol
                        name = name.strip()
                        symbol = symbol.strip()
                        
                        # Avoid duplicates
                        if (name, symbol) not in stock_results:
                            stock_results.append((name, symbol))
                            
                    except Exception as e:
                        continue
                        
            return stock_results[:limit]
            
        except Exception as e:
            # If yfinance search fails, return empty list
            return []
    
    def get_stock_info_yfinance(self, symbol: str) -> Dict[str, str]:
        """
        Get enhanced stock information using yfinance Ticker
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Extract relevant information
            stock_info = {
                'symbol': symbol,
                'name': info.get('longName') or info.get('shortName', symbol),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'country': info.get('country', 'Unknown'),
                'exchange': info.get('exchange', 'Unknown'),
                'market': self._determine_market(symbol, info.get('exchange', '')),
                'currency': info.get('currency', 'USD'),
                'market_cap': str(info.get('marketCap', 0)),
                'current_price': str(info.get('currentPrice', 0))
            }
            
            return stock_info
            
        except Exception as e:
            # Return basic info if yfinance fails
            return {
                'symbol': symbol,
                'name': symbol,
                'sector': 'Unknown',
                'industry': 'Unknown',
                'country': 'Unknown',
                'exchange': 'Unknown',
                'market': self._determine_market(symbol, ''),
                'currency': 'USD',
                'market_cap': '0',
                'current_price': '0'
            }
    
    def _determine_market(self, symbol: str, exchange: str) -> str:
        """
        Determine market based on symbol suffix and exchange
        """
        if symbol.endswith('.NS') or symbol.endswith('.BSE') or 'NSE' in exchange or 'BSE' in exchange:
            return 'India (NSE/BSE)'
        elif symbol.endswith('.L') or 'LSE' in exchange or 'LON' in exchange:
            return 'UK (LSE)'
        elif symbol.endswith('.T') or symbol.endswith('.TO') or 'TSE' in exchange or 'TYO' in exchange:
            return 'Japan (TSE)'
        elif symbol.endswith('.AX') or 'ASX' in exchange:
            return 'Australia (ASX)'
        elif symbol.endswith('.HK') or 'HKG' in exchange:
            return 'Hong Kong (HKSE)'
        elif symbol.endswith('.SS') or symbol.endswith('.SZ'):
            return 'China (SSE/SZSE)'
        elif symbol.endswith('.KS') or 'KRX' in exchange:
            return 'South Korea (KRX)'
        elif symbol.endswith('.DE') or 'XETRA' in exchange:
            return 'Germany (XETRA)'
        elif symbol.endswith('.PA') or 'EPA' in exchange:
            return 'France (Euronext)'
        elif symbol.endswith('.MI') or 'BIT' in exchange:
            return 'Italy (Borsa)'
        elif symbol.endswith('.TO') or 'TSX' in exchange:
            return 'Canada (TSX)'
        elif 'NASDAQ' in exchange or 'NYSE' in exchange or 'NYSEARCA' in exchange:
            return 'US (NASDAQ/NYSE)'
        else:
            return 'US (NASDAQ/NYSE)'  # Default to US market
    
    def validate_symbol(self, symbol: str) -> bool:
        """
        Validate if a symbol exists using yfinance
        """
        try:
            ticker = yf.Ticker(symbol)
            # Try to get basic info to validate
            info = ticker.info
            return bool(info and 'symbol' in info)
        except:
            return False
    
    def get_popular_stocks(self) -> List[Tuple[str, str]]:
        """
        Return a list of popular stocks for quick selection
        """
        popular_stocks = [
            ('Apple Inc.', 'AAPL'),
            ('Microsoft Corporation', 'MSFT'),
            ('Alphabet Inc.', 'GOOGL'),
            ('Amazon.com Inc.', 'AMZN'),
            ('Tesla Inc.', 'TSLA'),
            ('Meta Platforms Inc.', 'META'),
            ('NVIDIA Corporation', 'NVDA'),
            ('Reliance Industries Ltd.', 'RELIANCE.NS'),
            ('Tata Consultancy Services Ltd.', 'TCS.NS'),
            ('HDFC Bank Ltd.', 'HDFCBANK.NS'),
            ('Samsung Electronics Co. Ltd.', '005930.KS'),
            ('Taiwan Semiconductor Mfg.', 'TSM'),
            ('Toyota Motor Corporation', 'TM'),
            ('Nestlé S.A.', 'NESN.SW'),
            ('ASML Holding N.V.', 'ASML')
        ]
        return popular_stocks
    
    def get_trending_stocks(self) -> List[Tuple[str, str]]:
        """
        Get trending/popular stocks - for now return popular ones
        Could be enhanced with real trending data
        """
        return self.get_popular_stocks()
    
    def search_benchmarks_autocomplete(self, query: str, limit: int = 8) -> List[Tuple[str, str]]:
        """
        Search for benchmark indices based on query
        Returns list of tuples: (index_name, symbol)
        """
        benchmark_options = {
            # United States
            "S&P 500": "^GSPC",
            "NASDAQ Composite": "^IXIC", 
            "Dow Jones Industrial": "^DJI",
            "Russell 2000": "^RUT",
            "S&P MidCap 400": "^MID",
            "S&P SmallCap 600": "^SML",
            "NASDAQ 100": "^NDX",
            "VIX (Volatility)": "^VIX",
            
            # India
            "Nifty 50": "^NSEI",
            "Sensex (BSE 30)": "^BSESN",
            "Nifty Midcap 150": "NIFTYMIDCAP150.NS",
            "Nifty Smallcap 250": "NIFTYSMLCAP250.NS",
            "Nifty Next 50": "NIFTYJR.NS",
            "Nifty Bank": "^NSEBANK",
            "Nifty IT": "^CNXIT",
            "Nifty Auto": "^CNXAUTO",
            "Nifty Pharma": "^CNXPHARMA",
            "Nifty FMCG": "^CNXFMCG",
            "Nifty Energy": "^CNXENERGY",
            
            # Europe
            "FTSE 100 (UK)": "^FTSE",
            "DAX (Germany)": "^GDAXI",
            "CAC 40 (France)": "^FCHI",
            "FTSE MIB (Italy)": "FTSEMIB.MI",
            "IBEX 35 (Spain)": "^IBEX",
            "AEX (Netherlands)": "^AEX",
            "SMI (Switzerland)": "^SSMI",
            "ATX (Austria)": "^ATX",
            "BEL 20 (Belgium)": "^BFX",
            "PSI 20 (Portugal)": "PSI20.LS",
            "OMXS30 (Sweden)": "^OMX",
            "OBX (Norway)": "^OSEAX",
            "EURO STOXX 50": "^SX5E",
            
            # Asia Pacific
            "Nikkei 225 (Japan)": "^N225",
            "TOPIX (Japan)": "^TPX",
            "Hang Seng (Hong Kong)": "^HSI",
            "Shanghai Composite": "000001.SS",
            "CSI 300 (China)": "000300.SS",
            "Shenzhen Composite": "399001.SZ",
            "KOSPI (South Korea)": "^KS11",
            "KOSDAQ (South Korea)": "^KQ11",
            "ASX 200 (Australia)": "^AXJO",
            "ASX All Ordinaries": "^AORD",
            "STI (Singapore)": "^STI",
            "KLCI (Malaysia)": "^KLSE",
            "SET (Thailand)": "^SET.BK",
            "JSX (Indonesia)": "^JKSE",
            "PSEi (Philippines)": "^PSI",
            "TAIEX (Taiwan)": "^TWII",
            
            # Americas (Other)
            "TSX (Canada)": "^GSPTSE",
            "TSX Venture": "^JX",
            "Bovespa (Brazil)": "^BVSP",
            "IPC (Mexico)": "^MXX",
            "MERVAL (Argentina)": "^MERV",
            "IPSA (Chile)": "^IPSA",
            "IGBC (Colombia)": "^IGBC",
            
            # Middle East & Africa
            "TA-125 (Israel)": "^TA125.TA",
            "EGX 30 (Egypt)": "^CASE30",
            "TASI (Saudi Arabia)": "^TASI.SR",
            "JSE Top 40 (South Africa)": "^J203.JO",
            
            # Commodities & Others
            "Gold": "GC=F",
            "Silver": "SI=F",
            "Crude Oil (WTI)": "CL=F",
            "Brent Oil": "BZ=F",
            "Natural Gas": "NG=F",
            "Copper": "HG=F",
            "Bitcoin": "BTC-USD",
            "Ethereum": "ETH-USD",
            "DXY (US Dollar Index)": "DX-Y.NYB"
        }
        
        if len(query) < 1:
            return []
            
        query_lower = query.lower()
        matches = []
        
        for name, symbol in benchmark_options.items():
            # Check if query matches name or symbol
            if (query_lower in name.lower() or 
                query_lower in symbol.lower().replace('^', '').replace('=F', '')):
                matches.append((name, symbol))
                
        return matches[:limit]