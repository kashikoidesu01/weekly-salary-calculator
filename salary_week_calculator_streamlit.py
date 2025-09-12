#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Weekly Salary Calculator - Streamlit Web App
Fórmula: (Monto mensual / Días del mes) × Días de la semana × Número de semanas
"""
import streamlit as st

st.set_page_config(page_title="Weekly Salary Calculator", page_icon="🧮")

st.title("🧮 Weekly Salary Calculator")

# Fórmula en bonito (sin exponer nombres técnicos)
st.markdown("### 🧮 Fórmula")
st.latex(r"(\text{Monto mensual} \div \text{Días del mes}) \times \text{Días de la semana} \times \text{Número de semanas}")

with st.form("calc"):
    col1, col2 = st.columns(2)
    with col1:
        monthly_amount = st.number_input("💰 Monto mensual", min_value=0.0, value=650.0, step=10.0, format="%.2f")
        days_in_week = st.number_input("📆 Días de la semana a pagar", min_value=1, max_value=7, value=7, step=1)
    with col2:
        days_in_month = st.number_input("📅 Días del mes", min_value=28, max_value=31, value=30, step=1)
        weeks = st.number_input("🔢 Número de semanas", min_value=1, max_value=53, value=1, step=1)

    submitted = st.form_submit_button("Calcular")

def money(x: float) -> str:
    return f"${x:,.2f}"

if submitted:
    daily = monthly_amount / days_in_month if days_in_month else 0.0
    weekly = daily * days_in_week
    total = weekly * weeks

    st.subheader("Resultados")
    st.metric("Tarifa diaria", money(daily))
    st.metric("Pago por 1 semana", money(weekly))
    if weeks != 1:
        st.metric(f"Total por {int(weeks)} semana(s)", money(total))

st.markdown("---")
st.caption("Nota: Los meses no siempre tienen 4 semanas exactas. Usar días del mes lo hace justo en meses de 30 y 31 días (y en febrero).")

