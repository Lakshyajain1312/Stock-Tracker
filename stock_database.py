import yfinance as yf
import pandas as pd
import json
import requests
from typing import Dict, List, Tuple
import streamlit as st

class GlobalStockDatabase:
    """
    Comprehensive global stock database with real stock data
    """
    
    def __init__(self):
        self.stock_cache = {}
        self.comprehensive_stocks = self._load_comprehensive_stocks()
    
    def _load_comprehensive_stocks(self) -> Dict[str, str]:
        """
        Load a comprehensive database of global stocks from multiple sources
        """
        stocks = {}
        
        # Major US stocks (S&P 500 companies)
        us_stocks = {
            'Apple Inc.': 'AAPL', 'Microsoft Corporation': 'MSFT', 'Alphabet Inc.': 'GOOGL',
            'Amazon.com Inc.': 'AMZN', 'Tesla Inc.': 'TSLA', 'Meta Platforms Inc.': 'META',
            'NVIDIA Corporation': 'NVDA', 'Berkshire Hathaway Inc.': 'BRK-B',
            'UnitedHealth Group Inc.': 'UNH', 'Johnson & Johnson': 'JNJ',
            'JPMorgan Chase & Co.': 'JPM', 'Visa Inc.': 'V', 'Procter & Gamble Co.': 'PG',
            'Home Depot Inc.': 'HD', 'Mastercard Inc.': 'MA', 'Bank of America Corp.': 'BAC',
            'Chevron Corporation': 'CVX', 'Pfizer Inc.': 'PFE', 'Coca-Cola Co.': 'KO',
            'PepsiCo Inc.': 'PEP', 'Walmart Inc.': 'WMT', 'Walt Disney Co.': 'DIS',
            'Salesforce Inc.': 'CRM', 'Intel Corporation': 'INTC', 'Netflix Inc.': 'NFLX',
            'Adobe Inc.': 'ADBE', 'Cisco Systems Inc.': 'CSCO', 'Comcast Corporation': 'CMCSA',
            'Abbott Laboratories': 'ABT', 'Oracle Corporation': 'ORCL', 'Thermo Fisher Scientific Inc.': 'TMO',
            'Costco Wholesale Corporation': 'COST', 'Verizon Communications Inc.': 'VZ',
            'McDonald\'s Corporation': 'MCD', 'Nike Inc.': 'NKE', 'Exxon Mobil Corporation': 'XOM',
            'Merck & Co. Inc.': 'MRK', 'Eli Lilly and Co.': 'LLY', 'AbbVie Inc.': 'ABBV',
            'Advanced Micro Devices Inc.': 'AMD', 'Broadcom Inc.': 'AVGO',
            'IBM Corporation': 'IBM', 'General Electric Co.': 'GE', 'Ford Motor Co.': 'F',
            'General Motors Co.': 'GM', 'AT&T Inc.': 'T', 'Boeing Co.': 'BA',
            'Caterpillar Inc.': 'CAT', '3M Co.': 'MMM', 'American Express Co.': 'AXP',
            'Goldman Sachs Group Inc.': 'GS', 'Morgan Stanley': 'MS', 'Wells Fargo & Co.': 'WFC',
            'Citigroup Inc.': 'C', 'PayPal Holdings Inc.': 'PYPL', 'Uber Technologies Inc.': 'UBER',
            'Airbnb Inc.': 'ABNB', 'Zoom Video Communications Inc.': 'ZM',
            'Moderna Inc.': 'MRNA', 'Peloton Interactive Inc.': 'PTON',
            'Robinhood Markets Inc.': 'HOOD', 'Snowflake Inc.': 'SNOW',
            'CrowdStrike Holdings Inc.': 'CRWD', 'Palantir Technologies Inc.': 'PLTR',
            'Square Inc.': 'SQ', 'Shopify Inc.': 'SHOP', 'Spotify Technology S.A.': 'SPOT',
            'Twitter Inc.': 'TWTR', 'Snap Inc.': 'SNAP', 'Pinterest Inc.': 'PINS',
            'Unity Software Inc.': 'U', 'Roblox Corporation': 'RBLX', 'DocuSign Inc.': 'DOCU',
            'Slack Technologies Inc.': 'WORK', 'Zoom Video Communications': 'ZM'
        }
        stocks.update(us_stocks)
        
        # Indian stocks (NSE)
        indian_stocks = {
            'Reliance Industries Ltd.': 'RELIANCE.NS', 'Tata Consultancy Services Ltd.': 'TCS.NS',
            'HDFC Bank Ltd.': 'HDFCBANK.NS', 'Infosys Ltd.': 'INFY.NS',
            'Hindustan Unilever Ltd.': 'HINDUNILVR.NS', 'ICICI Bank Ltd.': 'ICICIBANK.NS',
            'State Bank of India': 'SBIN.NS', 'Bharti Airtel Ltd.': 'BHARTIARTL.NS',
            'ITC Ltd.': 'ITC.NS', 'Kotak Mahindra Bank Ltd.': 'KOTAKBANK.NS',
            'Asian Paints Ltd.': 'ASIANPAINT.NS', 'Larsen & Toubro Ltd.': 'LT.NS',
            'Axis Bank Ltd.': 'AXISBANK.NS', 'Maruti Suzuki India Ltd.': 'MARUTI.NS',
            'Sun Pharmaceutical Industries Ltd.': 'SUNPHARMA.NS', 'Wipro Ltd.': 'WIPRO.NS',
            'HCL Technologies Ltd.': 'HCLTECH.NS', 'Bajaj Finance Ltd.': 'BAJFINANCE.NS',
            'Titan Company Ltd.': 'TITAN.NS', 'Mahindra & Mahindra Ltd.': 'M&M.NS',
            'Tata Steel Ltd.': 'TATASTEEL.NS', 'JSW Steel Ltd.': 'JSWSTEEL.NS',
            'Coal India Ltd.': 'COALINDIA.NS', 'NTPC Ltd.': 'NTPC.NS',
            'Power Grid Corporation of India Ltd.': 'POWERGRID.NS',
            'Oil & Natural Gas Corporation Ltd.': 'ONGC.NS',
            'Indian Oil Corporation Ltd.': 'IOC.NS', 'Bharat Petroleum Corporation Ltd.': 'BPCL.NS',
            'Hindustan Petroleum Corporation Ltd.': 'HPCL.NS',
            'Tata Motors Ltd.': 'TATAMOTORS.NS', 'Bajaj Auto Ltd.': 'BAJAJ-AUTO.NS',
            'Hero MotoCorp Ltd.': 'HEROMOTOCO.NS', 'Eicher Motors Ltd.': 'EICHERMOT.NS',
            'Dr. Reddy\'s Laboratories Ltd.': 'DRREDDY.NS', 'Cipla Ltd.': 'CIPLA.NS',
            'Divi\'s Laboratories Ltd.': 'DIVISLAB.NS', 'Biocon Ltd.': 'BIOCON.NS',
            'Tech Mahindra Ltd.': 'TECHM.NS', 'Mindtree Ltd.': 'MINDTREE.NS',
            'Mphasis Ltd.': 'MPHASIS.NS', 'L&T Infotech Ltd.': 'LTI.NS',
            'Godrej Consumer Products Ltd.': 'GODREJCP.NS',
            'Britannia Industries Ltd.': 'BRITANNIA.NS', 'Nestle India Ltd.': 'NESTLEIND.NS',
            'Dabur India Ltd.': 'DABUR.NS', 'Marico Ltd.': 'MARICO.NS',
            'United Spirits Ltd.': 'UBL.NS', 'Varun Beverages Ltd.': 'VBL.NS'
        }
        stocks.update(indian_stocks)
        
        # European stocks
        european_stocks = {
            'ASML Holding N.V.': 'ASML', 'LVMH Moët Hennessy Louis Vuitton': 'MC.PA',
            'Nestlé S.A.': 'NESN.SW', 'SAP SE': 'SAP', 'Roche Holding AG': 'ROG.SW',
            'Novartis AG': 'NOVN.SW', 'Royal Dutch Shell plc': 'SHEL.L',
            'Unilever plc': 'ULVR.L', 'AstraZeneca plc': 'AZN.L', 'British Petroleum plc': 'BP.L',
            'Vodafone Group plc': 'VOD.L', 'BT Group plc': 'BT-A.L',
            'HSBC Holdings plc': 'HSBA.L', 'Barclays plc': 'BARC.L',
            'Lloyds Banking Group plc': 'LLOY.L', 'Standard Chartered plc': 'STAN.L',
            'Rio Tinto plc': 'RIO.L', 'BHP Group plc': 'BHP.L',
            'Glencore plc': 'GLEN.L', 'Anglo American plc': 'AAL.L',
            'Rolls-Royce Holdings plc': 'RR.L', 'BAE Systems plc': 'BA.L',
            'Airbus SE': 'AIR.PA', 'Siemens AG': 'SIE.DE', 'Volkswagen AG': 'VOW3.DE',
            'BMW AG': 'BMW.DE', 'Mercedes-Benz Group AG': 'MBG.DE',
            'Allianz SE': 'ALV.DE', 'Deutsche Bank AG': 'DBK.DE',
            'Commerzbank AG': 'CBK.DE', 'Bayer AG': 'BAYN.DE',
            'BASF SE': 'BAS.DE', 'Adidas AG': 'ADS.DE',
            'Puma SE': 'PUM.DE', 'Henkel AG & Co. KGaA': 'HEN3.DE'
        }
        stocks.update(european_stocks)
        
        # Asian stocks
        asian_stocks = {
            'Taiwan Semiconductor Manufacturing': 'TSM', 'Alibaba Group Holding Ltd.': 'BABA',
            'Tencent Holdings Ltd.': '0700.HK', 'Samsung Electronics Co. Ltd.': '005930.KS',
            'Toyota Motor Corporation': 'TM', 'Sony Group Corporation': 'SONY',
            'SoftBank Group Corp.': '9984.T', 'Nintendo Co. Ltd.': '7974.T',
            'Keyence Corporation': '6861.T', 'Recruit Holdings Co. Ltd.': '6098.T',
            'Tokyo Electron Ltd.': '8035.T', 'Shin-Etsu Chemical Co. Ltd.': '4063.T',
            'KDDI Corporation': '9433.T', 'NTT Data Corporation': '9613.T',
            'Mitsubishi UFJ Financial Group': '8306.T', 'Sumitomo Mitsui Financial Group': '8316.T',
            'China Construction Bank Corporation': '0939.HK', 'Industrial and Commercial Bank of China': '1398.HK',
            'Ping An Insurance Group Company of China': '2318.HK',
            'China Mobile Ltd.': '0941.HK', 'Meituan': '3690.HK',
            'JD.com Inc.': 'JD', 'NetEase Inc.': 'NTES',
            'Baidu Inc.': 'BIDU', 'PDD Holdings Inc.': 'PDD',
            'NIO Inc.': 'NIO', 'XPeng Inc.': 'XPEV', 'Li Auto Inc.': 'LI',
            'BYD Company Ltd.': '1211.HK', 'CATL': '300750.SZ',
            'Kweichow Moutai Co. Ltd.': '600519.SS', 'China Merchants Bank Co. Ltd.': '3968.HK'
        }
        stocks.update(asian_stocks)
        
        # Canadian stocks
        canadian_stocks = {
            'Shopify Inc.': 'SHOP.TO', 'Canadian National Railway Co.': 'CNR.TO',
            'Royal Bank of Canada': 'RY.TO', 'Toronto-Dominion Bank': 'TD.TO',
            'Bank of Nova Scotia': 'BNS.TO', 'Bank of Montreal': 'BMO.TO',
            'Canadian Imperial Bank of Commerce': 'CM.TO',
            'Brookfield Asset Management Inc.': 'BAM.TO', 'Canadian Pacific Railway Ltd.': 'CP.TO',
            'Enbridge Inc.': 'ENB.TO', 'TC Energy Corporation': 'TRP.TO',
            'Suncor Energy Inc.': 'SU.TO', 'Canadian Natural Resources Ltd.': 'CNQ.TO',
            'Nutrien Ltd.': 'NTR.TO', 'Barrick Gold Corporation': 'ABX.TO',
            'Franco-Nevada Corporation': 'FNV.TO', 'Agnico Eagle Mines Ltd.': 'AEM.TO'
        }
        stocks.update(canadian_stocks)
        
        # Australian stocks
        australian_stocks = {
            'BHP Group Ltd.': 'BHP.AX', 'Commonwealth Bank of Australia': 'CBA.AX',
            'CSL Ltd.': 'CSL.AX', 'Westpac Banking Corporation': 'WBC.AX',
            'Australia and New Zealand Banking Group': 'ANZ.AX',
            'National Australia Bank Ltd.': 'NAB.AX', 'Woolworths Group Ltd.': 'WOW.AX',
            'Telstra Corporation Ltd.': 'TLS.AX', 'Rio Tinto Ltd.': 'RIO.AX',
            'Fortescue Metals Group Ltd.': 'FMG.AX', 'Afterpay Ltd.': 'APT.AX',
            'Atlassian Corporation Plc': 'TEAM.AX', 'Xero Ltd.': 'XRO.AX'
        }
        stocks.update(australian_stocks)
        
        # Brazilian stocks
        brazilian_stocks = {
            'Petróleo Brasileiro S.A. - Petrobras': 'PBR', 'Vale S.A.': 'VALE',
            'Itaú Unibanco Holding S.A.': 'ITUB', 'Banco Bradesco S.A.': 'BBD',
            'Ambev S.A.': 'ABEV', 'Companhia Siderúrgica Nacional': 'SID',
            'Gerdau S.A.': 'GGB', 'Companhia de Bebidas das Américas': 'KOF',
            'Telefônica Brasil S.A.': 'VIV', 'Embraer S.A.': 'ERJ'
        }
        stocks.update(brazilian_stocks)
        
        return stocks
    
    def search_stocks_comprehensive(self, query: str) -> List[Tuple[str, str]]:
        """
        Enhanced search with comprehensive global stock database
        """
        if len(query) < 2:
            return []
        
        query_lower = query.lower().strip()
        results = []
        
        for company_name, symbol in self.comprehensive_stocks.items():
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
            # Company name word starts with query
            elif any(word.startswith(query_lower) for word in company_lower.split()):
                score = 60
            # Company name contains query
            elif query_lower in company_lower:
                score = 50
            # Fuzzy matching
            elif self._advanced_fuzzy_match(query_lower, company_lower, symbol_lower):
                score = 40
            
            if score > 0:
                results.append((company_name, symbol, score))
        
        # Sort by score and return top results
        results.sort(key=lambda x: (-x[2], len(x[0])))
        return [(name, symbol) for name, symbol, score in results[:15]]
    
    def _advanced_fuzzy_match(self, query: str, company: str, symbol: str) -> bool:
        """
        Advanced fuzzy matching for global stocks
        """
        # Common company keywords and abbreviations
        fuzzy_patterns = {
            'bank': ['bank', 'banking', 'financial', 'finance'],
            'tech': ['technology', 'technologies', 'software', 'systems'],
            'pharma': ['pharmaceutical', 'pharma', 'biotech', 'bio'],
            'auto': ['automotive', 'motor', 'motors', 'auto'],
            'oil': ['petroleum', 'energy', 'oil', 'gas'],
            'telecom': ['telecommunications', 'telecom', 'mobile', 'communications'],
            'retail': ['retail', 'stores', 'mart', 'market'],
            'insurance': ['insurance', 'life', 'assurance'],
            'mining': ['mining', 'metals', 'steel', 'gold'],
            'airline': ['airlines', 'air', 'aviation'],
            'electric': ['electric', 'power', 'energy', 'utilities'],
            'food': ['food', 'beverages', 'consumer']
        }
        
        query_words = query.split()
        for word in query_words:
            if word in fuzzy_patterns:
                for pattern in fuzzy_patterns[word]:
                    if pattern in company.lower() or pattern in symbol.lower():
                        return True
        
        # Check for partial matches in company sectors
        sector_keywords = ['ltd', 'inc', 'corp', 'corporation', 'company', 'group', 'holdings']
        for keyword in sector_keywords:
            if query in keyword or keyword in query:
                return False  # Don't match on generic corporate terms
        
        return False
    
    def get_stock_info_enhanced(self, symbol: str) -> dict:
        """
        Get enhanced stock information with sector and market details
        """
        try:
            if symbol in self.stock_cache:
                return self.stock_cache[symbol]
            
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Determine market/exchange from symbol
            market = "Unknown"
            if symbol.endswith('.NS'):
                market = "NSE (India)"
            elif symbol.endswith('.TO'):
                market = "TSX (Canada)"
            elif symbol.endswith('.L'):
                market = "LSE (UK)"
            elif symbol.endswith('.AX'):
                market = "ASX (Australia)"
            elif symbol.endswith('.HK'):
                market = "HKEX (Hong Kong)"
            elif symbol.endswith('.T'):
                market = "TSE (Japan)"
            elif symbol.endswith('.PA'):
                market = "Euronext Paris"
            elif symbol.endswith('.DE'):
                market = "XETRA (Germany)"
            elif '.' not in symbol:
                market = "NASDAQ/NYSE (US)"
            
            enhanced_info = {
                'name': info.get('longName', symbol),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'market_cap': info.get('marketCap', 0),
                'currency': info.get('currency', 'USD'),
                'market': market,
                'country': info.get('country', 'Unknown'),
                'website': info.get('website', ''),
                'business_summary': info.get('longBusinessSummary', '')[:200] + '...' if info.get('longBusinessSummary') else ''
            }
            
            self.stock_cache[symbol] = enhanced_info
            return enhanced_info
            
        except Exception as e:
            return {
                'name': symbol,
                'sector': 'Unknown',
                'industry': 'Unknown',
                'market_cap': 0,
                'currency': 'USD',
                'market': 'Unknown',
                'country': 'Unknown',
                'website': '',
                'business_summary': ''
            }
    
    def validate_symbol_enhanced(self, symbol: str) -> bool:
        """
        Enhanced symbol validation with better error handling
        """
        try:
            ticker = yf.Ticker(symbol)
            recent_data = ticker.history(period="5d", timeout=10)
            return not recent_data.empty
        except:
            return False
    
    def get_similar_stocks(self, symbol: str, limit: int = 5) -> List[Tuple[str, str]]:
        """
        Get similar stocks based on sector and market
        """
        try:
            stock_info = self.get_stock_info_enhanced(symbol)
            sector = stock_info.get('sector', '')
            market = stock_info.get('market', '')
            
            similar = []
            for company, stock_symbol in self.comprehensive_stocks.items():
                if stock_symbol != symbol:
                    other_info = self.get_stock_info_enhanced(stock_symbol)
                    if (other_info.get('sector') == sector or 
                        other_info.get('market') == market):
                        similar.append((company, stock_symbol))
                        if len(similar) >= limit:
                            break
            
            return similar
        except:
            return []