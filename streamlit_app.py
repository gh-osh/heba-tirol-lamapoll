import streamlit as st
import requests
import json
import pandas as pd
import datetime

today = datetime.date.today()
st.markdown("**HeBA/Tirol/OSQ/Report**")
st.badge(str(today))

lama_api_key= st.secrets["lamapoll_api_key"]

url = 'https://app.lamapoll.de/api/v2/polls/1965090/statistics'
headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer '+str(lama_api_key)
}
params = {
    'interval': 'day',
    'include[]': 'participants'
}

try:
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
    data = response.json()
    #print(json.dumps(data, indent=2))
except requests.exceptions.RequestException as e:
    st.write(f"Error making API request: {e}")
except json.JSONDecodeError:
    st.write(f"Error decoding JSON response. Response content: {response.text}")


dates = []
started_participants = []
finished_participants = []
visitors = []

for entry in data:
    dates.append(pd.to_datetime(entry['startDate']))
    participants_data = entry['participants']
    started_participants.append(participants_data['started'])
    finished_participants.append(participants_data['finished'])
    visitors.append(participants_data['visitors'])

st.success("Data extraction complete. Lists are ready for DataFrame creation.")

df = pd.DataFrame({
    'Date': dates,
    'Started': started_participants,
    'Finished': finished_participants,
    'Visitors': visitors
})
df = df.set_index('Date')

st.success("DataFrame created successfully with 'Date' as index.")
#df.head()
st.line_chart(df)

## Devices data
url = 'https://app.lamapoll.de/api/v2/polls/1965090/statistics'
headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer '+str(lama_api_key)
}
params = {
    'include[]': 'userDevices'
}

try:
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
    data_devices = response.json()
    #print(json.dumps(data, indent=2))
except requests.exceptions.RequestException as e:
    print(f"Error making API request: {e}")
except json.JSONDecodeError:
    print(f"Error decoding JSON response. Response content: {response.text}")

# Extract the userDevices data, which is a list of dictionaries
devices_data = data_devices[0]['userDevices']

# Create a DataFrame
df_devices = pd.DataFrame(devices_data)

print("DataFrame 'df_devices' created successfully.")
# Display the first few rows of the DataFrame
# df_devices.head()
#st.bar_chart(df_devices[['os','cnt']])
device_counts = df_devices.groupby(['deviceType'])['cnt'].sum().reset_index()
device_counts = device_counts.set_index('deviceType')
st.bar_chart(device_counts)
os_counts = df_devices.groupby(['os'])['cnt'].sum().reset_index()
os_counts = os_counts.set_index('os')
st.bar_chart(os_counts)
browser_counts = df_devices.groupby(['browser'])['cnt'].sum().reset_index()
browser_counts = browser_counts.set_index('browser')
st.bar_chart(browser_counts, color='grey')