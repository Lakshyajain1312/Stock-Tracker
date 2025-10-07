import streamlit as st
from typing import List, Tuple, Optional
from yfinance_search import YFinanceStockSearch

def stock_autocomplete(
    label: str,
    placeholder: str,
    key: str,
    yfinance_search: YFinanceStockSearch,
    help_text: Optional[str] = None
) -> Optional[Tuple[str, str]]:
    """
    Create an autocomplete stock search component
    Returns (company_name, symbol) tuple when selected, None otherwise
    """
    
    # Initialize session state for this component
    if f"{key}_query" not in st.session_state:
        st.session_state[f"{key}_query"] = ""
    if f"{key}_selected" not in st.session_state:
        st.session_state[f"{key}_selected"] = None
    if f"{key}_show_suggestions" not in st.session_state:
        st.session_state[f"{key}_show_suggestions"] = False
    
    # Create the search input
    st.markdown(f'<h4 style="color: #333333;">{label}</h4>', unsafe_allow_html=True)
    
    search_query = st.text_input(
        label,
        value=st.session_state[f"{key}_query"],
        placeholder=placeholder,
        key=f"{key}_input",
        help=help_text,
        label_visibility="collapsed"
    )
    
    # Ensure search_query is a string
    if search_query is None:
        search_query = ""
    
    # Track if query changed
    if search_query != st.session_state[f"{key}_query"]:
        st.session_state[f"{key}_query"] = search_query
        st.session_state[f"{key}_show_suggestions"] = len(search_query) >= 2
        if len(search_query) < 2:
            st.session_state[f"{key}_selected"] = None
    
    # Show autocomplete suggestions
    if st.session_state[f"{key}_show_suggestions"] and len(search_query) >= 2:
        try:
            search_results = yfinance_search.search_stocks_autocomplete(search_query, limit=6)
            
            if search_results:
                 st.markdown(f'<div style="background: linear-gradient(135deg, #1a1a1a 0%, #333333 100%); padding: 0.5rem; border-radius: 6px; margin: 0.5rem 0; border: 1px solid #e8e8e8;"><span style="color: white; font-weight: 500;">💡 {len(search_results)} suggestions</span></div>', unsafe_allow_html=True)


                
                # Create columns for suggestions
                cols = st.columns(2)
                for i, (company, symbol) in enumerate(search_results):
                    stock_info = yfinance_search.get_stock_info_yfinance(symbol)
                    market_emoji = "🇺🇸" if "US" in stock_info['market'] else "🇮🇳" if "India" in stock_info['market'] else "🇬🇧" if "UK" in stock_info['market'] else "🇯🇵" if "Japan" in stock_info['market'] else "🌍"
                    
                    with cols[i % 2]:
                        if st.button(
                            f"{market_emoji} {company[:25]}... ({symbol})" if len(company) > 25 else f"{market_emoji} {company} ({symbol})",
                            key=f"{key}_suggestion_{i}_{symbol}",
                            help=f"{symbol} • {stock_info['market']} • {stock_info.get('sector', 'Unknown')}",
                            use_container_width=True
                        ):
                            st.session_state[f"{key}_selected"] = (company, symbol)
                            st.session_state[f"{key}_query"] = f"{company} ({symbol})"
                            st.session_state[f"{key}_show_suggestions"] = False
                            st.rerun()
            else:
                st.markdown('<div style="background: #f5f5f5; padding: 0.5rem; border-radius: 6px; color: #666666; text-align: center; margin: 0.5rem 0; border: 1px solid #e0e0e0;">🔍 No matches found. Try a different search term.</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.markdown('<div style="background: #f5f5f5; padding: 0.5rem; border-radius: 6px; color: #666666; text-align: center; margin: 0.5rem 0; border: 1px solid #e0e0e0;">⚠️ Search temporarily unavailable</div>', unsafe_allow_html=True)
    
    elif len(search_query) > 0 and len(search_query) < 2:
        st.markdown('<div style="background: #f0f8ff; padding: 0.5rem; border-radius: 6px; color: #555555; text-align: center; margin: 0.5rem 0; border: 1px solid #ddeeff;">💡 Type at least 2 characters to see suggestions</div>', unsafe_allow_html=True)
    
    # Show current selection
    if st.session_state[f"{key}_selected"]:
        company, symbol = st.session_state[f"{key}_selected"]
        st.markdown(f'<div style="background: #e8f5e8; padding: 0.75rem; border-radius: 6px; color: #1a1a1a; text-align: center; margin: 0.5rem 0; font-weight: 500; border: 1px solid #c3e6c3;">✅ Selected: {company} ({symbol})</div>', unsafe_allow_html=True)
        return st.session_state[f"{key}_selected"]
    
    return None

def benchmark_autocomplete(
    label: str,
    placeholder: str,
    key: str,
    yfinance_search: YFinanceStockSearch,
    help_text: Optional[str] = None
) -> Optional[Tuple[str, str]]:
    """
    Create an autocomplete benchmark search component
    Returns (benchmark_name, symbol) tuple when selected, None otherwise
    """
    
    # Initialize session state for this component
    if f"{key}_query" not in st.session_state:
        st.session_state[f"{key}_query"] = ""
    if f"{key}_selected" not in st.session_state:
        st.session_state[f"{key}_selected"] = None
    if f"{key}_show_suggestions" not in st.session_state:
        st.session_state[f"{key}_show_suggestions"] = False
    
    # Create the search input
    st.markdown(f'<h4 style="color: #333333;">{label}</h4>', unsafe_allow_html=True)
    
    search_query = st.text_input(
        label,
        value=st.session_state[f"{key}_query"],
        placeholder=placeholder,
        key=f"{key}_input",
        help=help_text,
        label_visibility="collapsed"
    )
    
    # Ensure search_query is a string
    if search_query is None:
        search_query = ""
    
    # Track if query changed
    if search_query != st.session_state[f"{key}_query"]:
        st.session_state[f"{key}_query"] = search_query
        st.session_state[f"{key}_show_suggestions"] = len(search_query) >= 1
        if len(search_query) < 1:
            st.session_state[f"{key}_selected"] = None
    
    # Show autocomplete suggestions
    if st.session_state[f"{key}_show_suggestions"] and len(search_query) >= 1:
        try:
            search_results = yfinance_search.search_benchmarks_autocomplete(search_query, limit=6)
            
            if search_results:
                st.markdown(f'<div style="background: linear-gradient(135deg, #1a1a1a 0%, #333333 100%); padding: 0.5rem; border-radius: 6px; margin: 0.5rem 0; border: 1px solid #e8e8e8;"><span style="color: white; font-weight: 500;">💡 {len(search_results)} benchmark suggestions</span></div>', unsafe_allow_html=True)
                
                # Create columns for suggestions
                cols = st.columns(2)
                for i, (name, symbol) in enumerate(search_results):
                    # Determine flag/emoji based on name
                    emoji = "🇺🇸" if any(x in name for x in ["S&P", "NASDAQ", "Dow", "Russell", "VIX"]) else "🇮🇳" if "Nifty" in name or "Sensex" in name else "🇬🇧" if "FTSE" in name else "🇩🇪" if "DAX" in name else "🇯🇵" if "Nikkei" in name or "TOPIX" in name else "🌍"
                    
                    with cols[i % 2]:
                        if st.button(
                            f"{emoji} {name[:20]}..." if len(name) > 20 else f"{emoji} {name}",
                            key=f"{key}_suggestion_{i}_{symbol}",
                            help=f"{symbol} • {name}",
                            use_container_width=True
                        ):
                            st.session_state[f"{key}_selected"] = (name, symbol)
                            st.session_state[f"{key}_query"] = f"{name}"
                            st.session_state[f"{key}_show_suggestions"] = False
                            st.rerun()
            else:
                st.markdown('<div style="background: #f5f5f5; padding: 0.5rem; border-radius: 6px; color: #666666; text-align: center; margin: 0.5rem 0; border: 1px solid #e0e0e0;">🔍 No benchmark matches found. Try "S&P", "Nifty", "FTSE", etc.</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.markdown('<div style="background: #f5f5f5; padding: 0.5rem; border-radius: 6px; color: #666666; text-align: center; margin: 0.5rem 0; border: 1px solid #e0e0e0;">⚠️ Search temporarily unavailable</div>', unsafe_allow_html=True)
    
    # Show current selection
    if st.session_state[f"{key}_selected"]:
        name, symbol = st.session_state[f"{key}_selected"]
        st.markdown(f'<div style="background: #e8f5e8; padding: 0.75rem; border-radius: 6px; color: #1a1a1a; text-align: center; margin: 0.5rem 0; font-weight: 500; border: 1px solid #c3e6c3;">✅ Selected: {name} ({symbol})</div>', unsafe_allow_html=True)
        return st.session_state[f"{key}_selected"]
    
    return None
