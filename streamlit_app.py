import streamlit as st
import requests
import json
import pandas as pd
import datetime
import altair as alt


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
    st.success('API request successful. Data retrieved and parsed as JSON.')
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

#st.success("Data extraction complete. Lists are ready for DataFrame creation.")

df = pd.DataFrame({
    'Date': dates,
    'Started': started_participants,
    'Finished': finished_participants,
    'Visitors': visitors
})
df = df.set_index('Date')

#st.success("DataFrame created successfully with 'Date' as index.")
#df.head()
st.line_chart(df, color=['#7AAACE', '#355872', '#9CD5FF'])

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
#st.dataframe(df_devices)

col1, col2, col3 = st.columns(3)

with col1:
    browser = alt.Chart(df_devices).mark_bar().encode(
        x='browser',
        y='sum(cnt)'
    )
    st.altair_chart(browser, theme="streamlit", use_container_width=True)
with col2:
    devices = alt.Chart(df_devices).mark_bar().encode(
        x='deviceType',
        y='sum(cnt)'
    )
    st.altair_chart(devices, theme="streamlit", use_container_width=True)
with col3:
    os = alt.Chart(df_devices).mark_bar().encode(
        x='os',
        y='sum(cnt)'
    )
    st.altair_chart(os, theme="streamlit", use_container_width=True)