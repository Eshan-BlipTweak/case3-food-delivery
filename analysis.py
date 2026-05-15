import pandas as pd
import numpy as np
from prophet import Prophet
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
    daily = city_df.groupby('date').size().reset_index(name='y')
    daily['ds'] = pd.to_datetime(daily['date'])
    daily = daily[['ds', 'y']]

    m = Prophet(
        yearly_seasonality=False,
        weekly_seasonality=True,
        daily_seasonality=False,
        changepoint_prior_scale=0.05
    )
    m.fit(daily)

    future = m.make_future_dataframe(periods=periods)
    forecast = m.predict(future)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods + 14)

def peak_hours_per_city(df):
    grouped = df.groupby(['city', 'hour']).size().reset_index(name='orders')
    idx = grouped.groupby('city')['orders'].idxmax()
    return grouped.loc[idx].sort_values('orders', ascending=False)

def avg_delivery_by_surge(df):
    return df.groupby('surge_applied')['delivery_time_min'].mean().reset_index()