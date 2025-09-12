#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Weekly Salary Calculator - Streamlit Web App
Formula: (monthly_amount / days_in_month) * days_in_week * number_of_weeks
"""
import streamlit as st

st.set_page_config(page_title="Weekly Salary Calculator", page_icon="🧮")

st.title("🧮 Weekly Salary Calculator")
st.write("Formula: **(monthly_amount / days_in_month) × days_in_week × number_of_weeks**")

with st.form("calc"):
    col1, col2 = st.columns(2)
    with col1:
        monthly_amount = st.number_input("Monthly amount", min_value=0.0, value=650.0, step=10.0, format="%.2f")
        days_in_week = st.number_input("Days in week to pay", min_value=1, max_value=7, value=7, step=1)
    with col2:
        days_in_month = st.number_input("Days in month", min_value=28, max_value=31, value=30, step=1)
        weeks = st.number_input("Number of weeks", min_value=1, max_value=53, value=1, step=1)

    submitted = st.form_submit_button("Calculate")

def money(x: float) -> str:
    return f"${x:,.2f}"

if submitted:
    daily = monthly_amount / days_in_month if days_in_month else 0.0
    weekly = daily * days_in_week
    total = weekly * weeks

    st.subheader("Results")
    st.metric("Daily rate", money(daily))
    st.metric("1-week pay", money(weekly))
    if weeks != 1:
        st.metric(f"Total for {weeks} week(s)", money(total))

st.markdown("---")
st.caption("Tip: Months are not always 4 exact weeks. Using days-in-month keeps it fair in 30 vs 31-day months (and February).")
