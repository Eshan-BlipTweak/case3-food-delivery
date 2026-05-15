import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def load_data(path="case3_food_delivery_orders.csv"):
    df = pd.read_csv(path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.day_name()
    df['date'] = df['timestamp'].dt.date
    df['week'] = df['timestamp'].dt.isocalendar().week
    return df

def hourly_demand(df):
    return df.groupby('hour').size().reset_index(name='orders')

def daily_demand(df):
    return df.groupby('date').size().reset_index(name='orders')

def demand_by_city(df):
    return df.groupby(['city', 'hour']).size().reset_index(name='orders')

def demand_by_dow(df):
    order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    d = df.groupby('day_of_week').size().reset_index(name='orders')
    d['day_of_week'] = pd.Categorical(d['day_of_week'], categories=order, ordered=True)
    return d.sort_values('day_of_week')

def cuisine_revenue(df):
    return df.groupby('cuisine')['order_value'].sum().reset_index().sort_values('order_value', ascending=False)

def surge_analysis(df):
    surge = df.groupby('city')['surge_applied'].agg(['sum','count']).reset_index()
    surge['surge_pct'] = (surge['sum'] / surge['count'] * 100).round(1)
    return surge.sort_values('surge_pct', ascending=False)

def forecast_city(df, city='Delhi', periods=7):
    city_df = df[df['city'] == city].copy()
    daily = city_df.groupby('date').size().reset_index(name='orders')
    daily['ds'] = pd.to_datetime(daily['date'])
    daily = daily.sort_values('ds')
    
    # 7-day rolling average as baseline
    daily['rolling'] = daily['orders'].rolling(7, min_periods=1).mean()
    
    # Simple trend: last 7 days avg
    last_7 = daily['orders'].tail(7).mean()
    last_14 = daily['orders'].tail(14).mean()
    trend = (last_7 - last_14) / last_14 if last_14 > 0 else 0
    
    # Forecast next 7 days
    last_date = daily['ds'].max()
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=periods)
    future_orders = [last_7 * (1 + trend * i) for i in range(1, periods + 1)]
    future_upper = [v * 1.15 for v in future_orders]
    future_lower = [v * 0.85 for v in future_orders]
    
    forecast = pd.DataFrame({
        'ds': future_dates,
        'yhat': future_orders,
        'yhat_upper': future_upper,
        'yhat_lower': future_lower
    })
    
    # Include last 14 days of actuals for context
    historical = daily.tail(14)[['ds', 'orders']].rename(columns={'orders': 'yhat'})
    historical['yhat_upper'] = historical['yhat']
    historical['yhat_lower'] = historical['yhat']
    
    return pd.concat([historical, forecast], ignore_index=True)

def peak_hours_per_city(df):
    grouped = df.groupby(['city', 'hour']).size().reset_index(name='orders')
    idx = grouped.groupby('city')['orders'].idxmax()
    return grouped.loc[idx].sort_values('orders', ascending=False)

def avg_delivery_by_surge(df):
    return df.groupby('surge_applied')['delivery_time_min'].mean().reset_index()