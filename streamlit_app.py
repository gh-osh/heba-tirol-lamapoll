import streamlit as st

st.title("Tirol")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import requests
import json
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

import pandas as pd

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

import matplotlib.pyplot as plt

# Set a larger figure size for better readability
plt.figure(figsize=(12, 6))

# Create the line plot with specified line styles and colors
df.plot(ax=plt.gca(), linewidth=2, style=['-', '--', ':'], color=['#1f77b4', '#aec7e8', '#4c78a8'])

# Add plot title and labels
plt.title('Daily Participant Trends Over Time', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Number of Participants/Visitors', fontsize=12)

# Add a legend
plt.legend(['Started Participants', 'Finished Participants', 'Visitors'], loc='upper left', bbox_to_anchor=(1, 1))

# Improve layout for legends outside the plot
plt.tight_layout()

# Display the plot
st.pyplot(plt.show())

st.line_chart(df)