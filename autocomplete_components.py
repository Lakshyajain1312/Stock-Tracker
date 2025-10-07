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
    Create an autocomplete stock search component.
    Returns (company_name, symbol) tuple when selected, None otherwise.
    """

    # ---- Session state ----
    if f"{key}_query" not in st.session_state:
        st.session_state[f"{key}_query"] = ""
    if f"{key}_selected" not in st.session_state:
        st.session_state[f"{key}_selected"] = None
    if f"{key}_show_suggestions" not in st.session_state:
        st.session_state[f"{key}_show_suggestions"] = False

    # ---- Input ----
    st.markdown(f'<h4 style="color:#333333;">{label}</h4>', unsafe_allow_html=True)
    search_query = st.text_input(
        label,
        value=st.session_state[f"{key}_query"],
        placeholder=placeholder,
        key=f"{key}_input",
        help=help_text,
        label_visibility="collapsed",
    )

    if search_query is None:
        search_query = ""

    # Track changes
    if search_query != st.session_state[f"{key}_query"]:
        st.session_state[f"{key}_query"] = search_query
        st.session_state[f"{key}_show_suggestions"] = len(search_query) >= 2
        if len(search_query) < 2:
            st.session_state[f"{key}_selected"] = None

    # ---- Suggestions ----
    if st.session_state[f"{key}_show_suggestions"] and len(search_query) >= 2:
        try:
            search_results = yfinance_search.search_stocks_autocomplete(search_query, limit=6)

            if search_results:
                # WHITE suggestions header
                st.markdown(
                    f"""
<div style="
  background:#ffffff;
  padding:0.5rem;
  border-radius:6px;
  margin:0.5rem 0;
  border:1px solid #e0e0e0;
  box-shadow:0 2px 4px rgba(0,0,0,0.05);
">
  <span style="color:#000000;font-weight:500;">💡 {len(search_results)} suggestions</span>
</div>
""",
                    unsafe_allow_html=True,
                )

                cols = st.columns(2)
                for i, (company, symbol) in enumerate(search_results):
                    stock_info = yfinance_search.get_stock_info_yfinance(symbol)
                    market = stock_info.get("market", "")
                    if "US" in market:
                        flag = "🇺🇸"
                    elif "India" in market:
                        flag = "🇮🇳"
                    elif "UK" in market:
                        flag = "🇬🇧"
                    elif "Japan" in market:
                        flag = "🇯🇵"
                    else:
                        flag = "🌍"

                    label_text = f"{flag} {company} ({symbol})"
                    if len(company) > 25:
                        label_text = f"{flag} {company[:25]}... ({symbol})"

                    with cols[i % 2]:
                        if st.button(
                            label_text,
                            key=f"{key}_suggestion_{i}_{symbol}",
                            help=f"{symbol} • {market} • {stock_info.get('sector', 'Unknown')}",
                            use_container_width=True,
                        ):
                            st.session_state[f"{key}_selected"] = (company, symbol)
                            st.session_state[f"{key}_query"] = f"{company} ({symbol})"
                            st.session_state[f"{key}_show_suggestions"] = False
                            st.rerun()
            else:
                st.markdown(
                    '<div style="background:#f5f5f5;padding:0.5rem;border-radius:6px;color:#666;text-align:center;margin:0.5rem 0;border:1px solid #e0e0e0;">🔍 No matches found. Try a different search term.</div>',
                    unsafe_allow_html=True,
                )
        except Exception:
            st.markdown(
                '<div style="background:#f5f5f5;padding:0.5rem;border-radius:6px;color:#666;text-align:center;margin:0.5rem 0;border:1px solid #e0e0e0;">⚠️ Search temporarily unavailable</div>',
                unsafe_allow_html=True,
            )

    elif 0 < len(search_query) < 2:
        st.markdown(
            '<div style="background:#f0f8ff;padding:0.5rem;border-radius:6px;color:#555;text-align:center;margin:0.5rem 0;border:1px solid #ddeeff;">💡 Type at least 2 characters to see suggestions</div>',
            unsafe_allow_html=True,
        )

    # ---- Selected ----
    if st.session_state[f"{key}_selected"]:
        company, symbol = st.session_state[f"{key}_selected"]
        st.markdown(
            f'<div style="background:#e8f5e8;padding:0.75rem;border-radius:6px;color:#1a1a1a;text-align:center;margin:0.5rem 0;font-weight:500;border:1px solid #c3e6c3;">✅ Selected: {company} ({symbol})</div>',
            unsafe_allow_html=True,
        )
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
    Create an autocomplete benchmark search component.
    Returns (benchmark_name, symbol) tuple when selected, None otherwise.
    """

    # ---- Session state ----
    if f"{key}_query" not in st.session_state:
        st.session_state[f"{key}_query"] = ""
    if f"{key}_selected" not in st.session_state:
        st.session_state[f"{key}_selected"] = None
    if f"{key}_show_suggestions" not in st.session_state:
        st.session_state[f"{key}_show_suggestions"] = False

    # ---- Input ----
    st.markdown(f'<h4 style="color:#333333;">{label}</h4>', unsafe_allow_html=True)
    search_query = st.text_input(
        label,
        value=st.session_state[f"{key}_query"],
        placeholder=placeholder,
        key=f"{key}_input",
        help=help_text,
        label_visibility="collapsed",
    )

    if search_query is None:
        search_query = ""

    if search_query != st.session_state[f"{key}_query"]:
        st.session_state[f"{key}_query"] = search_query
        st.session_state[f"{key}_show_suggestions"] = len(search_query) >= 1
        if len(search_query) < 1:
            st.session_state[f"{key}_selected"] = None

    # ---- Suggestions ----
    if st.session_state[f"{key}_show_suggestions"] and len(search_query) >= 1:
        try:
            search_results = yfinance_search.search_benchmarks_autocomplete(search_query, limit=6)

            if search_results:
                # WHITE benchmark suggestions header
                st.markdown(
                    f"""
<div style="
  background:#ffffff;
  padding:0.5rem;
  border-radius:6px;
  margin:0.5rem 0;
  border:1px solid #e0e0e0;
  box-shadow:0 2px 4px rgba(0,0,0,0.05);
">
  <span style="color:#000000;font-weight:500;">💡 {len(search_results)} benchmark suggestions</span>
</div>
""",
                    unsafe_allow_html=True,
                )

                cols = st.columns(2)
                for i, (name, symbol) in enumerate(search_results):
                    if any(x in name for x in ["S&P", "NASDAQ", "Dow", "Russell", "VIX"]):
                        emoji = "🇺🇸"
                    elif "Nifty" in name or "Sensex" in name:
                        emoji = "🇮🇳"
                    elif "FTSE" in name:
                        emoji = "🇬🇧"
                    elif "DAX" in name:
                        emoji = "🇩🇪"
                    elif "Nikkei" in name or "TOPIX" in name:
                        emoji = "🇯🇵"
                    else:
                        emoji = "🌍"

                    label_text = f"{emoji} {name}"
                    if len(name) > 20:
                        label_text = f"{emoji} {name[:20]}..."

                    with cols[i % 2]:
                        if st.button(
                            label_text,
                            key=f"{key}_suggestion_{i}_{symbol}",
                            help=f"{symbol} • {name}",
                            use_container_width=True,
                        ):
                            st.session_state[f"{key}_selected"] = (name, symbol)
                            st.session_state[f"{key}_query"] = name
                            st.session_state[f"{key}_show_suggestions"] = False
                            st.rerun()
            else:
                st.markdown(
                    '<div style="background:#f5f5f5;padding:0.5rem;border-radius:6px;color:#666;text-align:center;margin:0.5rem 0;border:1px solid #e0e0e0;">🔍 No benchmark matches found. Try "S&P", "Nifty", "FTSE", etc.</div>',
                    unsafe_allow_html=True,
                )
        except Exception:
            st.markdown(
                '<div style="background:#f5f5f5;padding:0.5rem;border-radius:6px;color:#666;text-align:center;margin:0.5rem 0;border:1px solid #e0e0e0;">⚠️ Search temporarily unavailable</div>',
                unsafe_allow_html=True,
            )

    # ---- Selected ----
    if st.session_state[f"{key}_selected"]:
        name, symbol = st.session_state[f"{key}_selected"]
        st.markdown(
            f'<div style="background:#e8f5e8;padding:0.75rem;border-radius:6px;color:#1a1a1a;text-align:center;margin:0.5rem 0;font-weight:500;border:1px solid #c3e6c3;">✅ Selected: {name} ({symbol})</div>',
            unsafe_allow_html=True,
        )
        return st.session_state[f"{key}_selected"]

    return None
