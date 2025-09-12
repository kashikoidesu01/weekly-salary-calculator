#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Weekly Salary Calculator - Streamlit Web App
Formula: (Monthly amount / Days in month) × Days in week × Number of weeks
Lets the user choose a base currency (default USD) and shows results in that currency.
"""
import streamlit as st

st.set_page_config(page_title="Weekly Salary Calculator", page_icon="🧮")

st.title("🧮 Weekly Salary Calculator")

# --- Currencies (extend as needed) ---
CURRENCIES = [
    ("USD", "US Dollar", "$"),
    ("EUR", "Euro", "€"),
    ("GBP", "British Pound", "£"),
    ("CAD", "Canadian Dollar", "$"),
    ("MXN", "Mexican Peso", "$"),
    ("COP", "Colombian Peso", "$"),
    ("BRL", "Brazilian Real", "R$"),
    ("CLP", "Chilean Peso", "$"),
    ("PEN", "Peruvian Sol", "S/"),
    ("JPY", "Japanese Yen", "¥"),
    ("ARS", "Argentine Peso", "$"),
]

def money(x: float, symbol: str="$") -> str:
    return f"{symbol}{x:,.2f}"

# Pretty formula display
st.markdown("### Formula")
st.latex(r"(\text{Monthly amount} \div \text{Days in month}) \times \text{Days in week} \times \text{Number of weeks}")

with st.form("calc"):
    # Currency selector (default USD)
    st.markdown("#### Base currency")
    labels = [f"{code} — {name}" for code, name, _ in CURRENCIES]
    default_idx = 0  # USD
    choice = st.selectbox("Select your currency", options=labels, index=default_idx)
    base_code, base_name, base_symbol = CURRENCIES[labels.index(choice)]

    col1, col2 = st.columns(2)
    with col1:
        monthly_amount = st.number_input(
            f"Monthly amount ({base_code})",
            min_value=0.0, value=650.00 if base_code == "USD" else 0.00,
            step=10.0, format="%.2f"
        )
        days_in_week = st.number_input("Days in week", min_value=1, max_value=7, value=7, step=1)
    with col2:
        days_in_month = st.number_input("Days in month", min_value=28, max_value=31, value=30, step=1)
        weeks = st.number_input("Number of weeks", min_value=1, max_value=53, value=1, step=1)

    submitted = st.form_submit_button("Calculate")

if submitted:
    daily = monthly_amount / days_in_month if days_in_month else 0.0
    weekly = daily * days_in_week
    total = weekly * weeks

    st.subheader(f"Results in {base_code}")
    st.metric("Daily rate", money(daily, base_symbol))
    st.metric("1-week pay", money(weekly, base_symbol))
    if weeks != 1:
        st.metric(f"Total for {int(weeks)} week(s)", money(total, base_symbol))

st.markdown("---")
st.caption("Tip: Months are not always exactly 4 weeks. Using days-in-month keeps things fair for 30 vs 31-day months (and February).")


