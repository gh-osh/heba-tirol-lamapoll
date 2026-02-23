import streamlit as st
import requests
import json
import pandas as pd
import datetime

today = datetime.date.today()
st.header("HeBA/Tirol/OSQ/Report")
st.subheader(today)

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

st.write("Data extraction complete. Lists are ready for DataFrame creation.")

df = pd.DataFrame({
    'Date': dates,
    'Started': started_participants,
    'Finished': finished_participants,
    'Visitors': visitors
})
df = df.set_index('Date')

st.write("DataFrame created successfully with 'Date' as index.")
#df.head()

st.line_chart(df)