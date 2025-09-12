# Weekly Salary Calculator

A simple Streamlit web app to calculate weekly pay using the proportional-days formula and (optionally) convert results to another currency.

**Formula**

\[
(\text{Monthly amount} \div \text{Days in month}) \times \text{Days in week} \times \text{Number of weeks}
\]

---

## Features

- Choose a **base currency** (default: USD) and enter your monthly amount in that currency.
- Calculate **daily rate**, **1-week pay**, and **total** for N weeks using the days-in-month approach (fair for 30 vs 31 days and February).
- Optional **currency conversion** of the calculated results to another currency.
- Shows **last updated** timestamp for FX rates and the **provider** used.
- Lightweight UI; no data is stored server-side.

---

## Live App

> Add your public URL here (Streamlit Cloud):
>
> `https://YOUR-APP-URL.streamlit.app`

---

## Supported Currencies (base & target)

USD, EUR, GBP, CAD, MXN, COP, BRL, CLP, PEN, JPY, ARS  
*(Easy to extend in code.)*

---

## Getting Started (Local)

### 1) Requirements
- Python 3.9+ recommended

Create/confirm `requirements.txt`:
