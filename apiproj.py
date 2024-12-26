import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import time

# API URL
API_URL = "https://api.thingspeak.com/channels/1596152/feeds.json?results=20"

# Function to fetch data from the API
def fetch_data():
    response = requests.get(API_URL)
    data = response.json()
    return data

# Function to extract and process data into a DataFrame
def extract_data(data):
    feeds = data['feeds']
    timestamps = [feed['created_at'] for feed in feeds]
    humidity = [feed['field1'] for feed in feeds]
    temp = [feed['field2'] for feed in feeds]
    co = [feed['field3'] for feed in feeds]
    pressure = [feed['field4'] for feed in feeds]
    light = [feed['field5'] for feed in feeds]
    pm2 = [feed['field6'] for feed in feeds]

    df = pd.DataFrame({
        'Time': pd.to_datetime(timestamps),
        'Humidity': pd.to_numeric(humidity),
        'Temperature': pd.to_numeric(temp),
        'CO': pd.to_numeric(co),
        'Pressure': pd.to_numeric(pressure),
        'Light Intensity': pd.to_numeric(light),
        'PM2.5': pd.to_numeric(pm2)
    })
    return df

# Streamlit app layout
st.title(" Data Dashboard")
st.write("Fetching data from API and displaying six line charts.")

# Fetch data and extract it
data = fetch_data()
df = extract_data(data)

# Display raw data (last 10 points)
st.write("### Latest 10 Data Points")
st.dataframe(df.tail(10))

# Plotting the charts
st.write("### Line Charts")

fig, axs = plt.subplots(3, 2, figsize=(12, 12))
fields = ['Humidity', 'Temperature', 'CO', 'Pressure', 'Light Intensity', 'PM2.5']

for i, field in enumerate(fields):
    row = i // 2
    col = i % 2
    axs[row, col].plot(df['Time'], df[field], marker='o')
    axs[row, col].set_title(f'{field} Over Time')
    axs[row, col].set_xlabel('Time')
    axs[row, col].set_ylabel(field)
    axs[row, col].tick_params(axis='x', rotation=30)

plt.tight_layout()
st.pyplot(fig)

# Auto-refresh every hour
st.write("Data refreshes automatically every hour.")
time.sleep(3600)  # 1 hour delay for refresh
