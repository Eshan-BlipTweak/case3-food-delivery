---
title: Case3 Food Delivery
emoji: 🍕
colorFrom: red
colorTo: yellow
sdk: docker
app_file: app.py
pinned: false
---

# Case 3: Food Delivery Demand Pulse

**Live demo:** https://eshtiw-case3-food-delivery.hf.space
**Repo:** https://github.com/Eshan-BlipTweak/case3-food-delivery
**Demo video:** https://www.youtube.com/watch?v=MgYcq999ppk

## What this is
An interactive demand analytics dashboard for a regional food delivery company across 7 Indian cities, built to help the Ops Head identify real peak demand windows and redesign rider incentive policy.

## How to run locally
1. `git clone https://github.com/Eshan-BlipTweak/case3-food-delivery`
2. `cd case3-food-delivery`
3. `pip install streamlit pandas plotly scikit-learn`
4. `streamlit run app.py`
5. Open http://localhost:8501

## Stack
- Streamlit — interactive dashboard, no frontend code needed
- Pandas — data wrangling and aggregation
- Plotly — interactive charts
- Rolling average — 7-day demand forecast, interpretable for non-technical audience
- HF Spaces (Docker) — free HTTPS deployment

## What's NOT done
- Live data pipeline — dataset is static CSV; production would pull from a warehouse
- Holiday/weather augmentation — would improve forecast accuracy
- Per-restaurant analysis — too granular for ops policy brief

## In production, I would also add
- Automated daily ingestion from the order management system
- Airflow pipeline replacing the static CSV
- Prophet or LSTM model with holiday calendar for better forecast accuracy
- Alerting when surge rate exceeds threshold
- Role-based access so Ops Head vs CFO see different views