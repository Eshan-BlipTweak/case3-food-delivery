# Decisions Log — Case 3

## Assumptions I made
1. "Peak demand" analysis is most actionable at hourly + day-of-week granularity — daily is too coarse for rider incentive policy
2. Delhi chosen as primary forecast city — highest order volume in dataset
3. Surge policy recommendations based on observed surge_applied patterns, not self-reported data
4. 7-day forecast horizon is sufficient for next month's ops planning

## Trade-offs
| Choice | Alternative | Why I picked this |
|---|---|---|
| Prophet | ARIMA / rolling mean | Handles weekly seasonality automatically, minimal tuning needed |
| Streamlit | Jupyter only | Ops Head can interact with data herself, not just read static charts |
| Plotly | Matplotlib | Interactive charts — evaluators can hover and explore |
| City-level surge analysis | Restaurant-level | More actionable for ops policy decisions |

## What I de-scoped and why
- Weather/holiday augmentation — no public holiday API integrated; would improve forecast accuracy in production
- Per-restaurant analysis — 800 restaurants too granular for a one-day ops brief
- A/B test design for recommendations — time constraint; noted as next step

## What I'd do differently with another day
- Add confidence intervals explanation for non-technical Ops Head
- Build cohort analysis comparing city tiers (metro vs non-metro)
- Integrate holiday calendar for better forecast accuracy
- Add data freshness indicator showing when pipeline last ran