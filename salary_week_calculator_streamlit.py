#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Weekly Salary Calculator - Streamlit Web App
- Base currency selector; Monthly amount resets to 0.00 when currency changes
- Optional conversion to a target currency using exchangerate.host
- Shows FX last-updated timestamp
"""
import datetime as dt
import requests
import streamlit as st

st.set_page_config(page_title="Weekly Salary Calculator", page_icon="🧮")
st.title("🧮 Weekly Salary Calculator")

# Currency definitions
CURRENCIES = [
    ("USD", "US Dollar", "$"), ("EUR", "Euro", "€"), ("GBP", "British Pound", "£"),
    ("CAD", "Canadian Dollar", "$"), ("MXN", "Mexican Peso", "$"),
    ("COP", "Colombian Peso", "$"), ("BRL", "Brazilian Real", "R$"),
    ("CLP", "Chilean Peso", "$"), ("PEN", "Peruvian Sol", "S/"),
    ("JPY", "Japanese Yen", "¥"), ("ARS", "Argentine Peso", "$"),
]
CODE_TO_NAME = {c: n for c, n, _ in CURRENCIES}
CODE_TO_SYMBOL = {c: s for c, _, s in CURRENCIES}
CODES = [c for c, _, _ in CURRENCIES]

def money(x: float, symbol: str="$") -> str:
    return f"{symbol}{x:,.2f}"

@st.cache_data(ttl=60*30)
def get_usd_rates():
    """Return (rates_dict, fetched_at_str_UTC)."""
    url = "https://api.exchangerate.host/latest?base=USD"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    data = r.json()
    rates = data.get("rates", {})
    fetched_at = dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    return rates, fetched_at

def usd_to(code: str, amount_usd: float) -> float:
    if code.upper() == "USD":
        return amount_usd
    rates, _ = get_usd_rates()
    rate = rates.get(code.upper())
    if rate is None:
        raise RuntimeError(f"Rate for {code} not available.")
    return amount_usd * float(rate)

# Pretty formula
st.markdown("### Formula")
st.latex(r"(\text{Monthly amount} \div \text{Days in month}) \times \text{Days in week} \times \text{Number of weeks}")

# ---- Session defaults
if "base_code" not in st.session_state:
    st.session_state.base_code = "USD"
if "monthly_amount" not in st.session_state:
    st.session_state.monthly_amount = 650.00  # default when USD

def on_currency_change():
    # When base currency changes, zero the monthly amount immediately
    st.session_state.monthly_amount = 0.00

# ---- Inputs
st.markdown("#### Base currency")
base_code = st.selectbox(
    "Select your currency",
    options=CODES,
    index=CODES.index(st.session_state.base_code),
    format_func=lambda c: f"{c} — {CODE_TO_NAME[c]}",
    key="base_code",
    on_change=on_currency_change,
)
base_symbol = CODE_TO_SYMBOL[base_code]

col1, col2 = st.columns(2)
with col1:
    # IMPORTANT: let the widget own the key; don't assign to session_state here
    monthly_amount = st.number_input(
        f"Monthly amount ({base_code})",
        min_value=0.0,
        value=float(st.session_state.monthly_amount),
        step=10.0,
        format="%.2f",
        key="monthly_amount",
    )
    days_in_week = st.number_input("Days in week", min_value=1, max_value=7, value=7, step=1)
with col2:
    days_in_month = st.number_input("Days in month", min_value=28, max_value=31, value=30, step=1)
    weeks = st.number_input("Number of weeks", min_value=1, max_value=53, value=1, step=1)

calc_clicked = st.button("Calculate")

# ---- Calculation
if calc_clicked:
    daily = (monthly_amount / days_in_month) if days_in_month else 0.0
    weekly = daily * days_in_week
    total = weekly * weeks
    st.session_state.results = {
        "base_code": base_code, "base_symbol": base_symbol,
        "daily": daily, "weekly": weekly, "total": total, "weeks": int(weeks),
    }

# ---- Results
if "results" in st.session_state:
    res = st.session_state.results
    st.subheader(f"Results in {res['base_code']}")
    st.metric("Daily rate", money(res["daily"], res["base_symbol"]))
    st.metric("1-week pay", money(res["weekly"], res["base_symbol"]))
    if res["weeks"] != 1:
        st.metric(f"Total for {res['weeks']} week(s)", money(res["total"], res["base_symbol"]))

    # Conversion section
    st.markdown("---")
    st.markdown("#### Convert results to another currency")
    target_code = st.selectbox(
        "Target currency",
        options=CODES,
        index=CODES.index("USD"),
        format_func=lambda c: f"{c} — {CODE_TO_NAME[c]}",
        key="target_code",
    )
    convert_clicked = st.button("Convert current results")

    if convert_clicked:
        try:
            # Convert base results to USD first
            if res["base_code"] == "USD":
                daily_usd, weekly_usd, total_usd = res["daily"], res["weekly"], res["total"]
            else:
                rates, _ = get_usd_rates()
                usd_to_base = rates.get(res["base_code"])
                if not usd_to_base:
                    raise RuntimeError(f"Rate for {res['base_code']} not available.")
                base_to_usd = 1.0 / float(usd_to_base)
                daily_usd = res["daily"] * base_to_usd
                weekly_usd = res["weekly"] * base_to_usd
                total_usd = res["total"] * base_to_usd

            # USD -> target
            rates, fetched_at = get_usd_rates()
            if target_code == "USD":
                daily_t, weekly_t, total_t = daily_usd, weekly_usd, total_usd
            else:
                rate_t = rates.get(target_code)
                if not rate_t:
                    raise RuntimeError(f"Rate for {target_code} not available.")
                daily_t = daily_usd * rate_t
                weekly_t = weekly_usd * rate_t
                total_t = total_usd * rate_t

            st.subheader(f"Converted to {target_code}")
            st.metric("Daily rate", f"{daily_t:,.2f} {target_code}")
            st.metric("1-week pay", f"{weekly_t:,.2f} {target_code}")
            if res["weeks"] != 1:
                st.metric(f"Total for {res['weeks']} week(s)", f"{total_t:,.2f} {target_code}")
            st.caption(f"Rates from exchangerate.host • updated: {fetched_at}")
        except Exception as e:
            st.error(f"Conversion error: {e}")

st.markdown("---")
st.caption("Note: Months are not always exactly 4 weeks. Using days-in-month keeps things fair for 30 vs 31-day months (and February).")

