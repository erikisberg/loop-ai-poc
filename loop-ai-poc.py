import streamlit as st
import requests
import pandas as pd
import datetime
import json

today = datetime.datetime.now()
next_year = today.year
jan_1 = datetime.date(next_year, 1, 1)
dec_31 = datetime.date(next_year, 12, 31)

min_year = 2020
max_year = 2030
min_date = datetime.date(min_year, 1, 1)
max_date = datetime.date(max_year, 12, 31)

# Streamlit UI Components
st.title("Impact Loop AI POC")
st.subheader("Utforska materialet på Impact Loop med hjälp av AI")
# st.write("Berätta mer om vad du är ute efter för material")
user_input = st.text_area("Berätta mer om vad du är ute efter för material?")
st.markdown("""
* _Vad har sagts om urban mobility de senaste 60 dagarna_
* _Aa_
* _Aa_
""", unsafe_allow_html=True)


# POST Request API
def send_post_request(input_text):
    url = "https://api.retool.com/v1/workflows/0f6b3d1c-ebfb-448c-adc2-ea29ee78673c/startTrigger?workflowApiKey=retool_wk_8bd8e86c029945c1a6f15a1c07b645f6"
    headers = {'Content-Type': 'application/json'}
    data = {
        "body": input_text, 
    }
    
    with st.spinner('Vi letar aktiviteter och rekommendationer...'):
        response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        response_data = response.json()
        data_field = response_data.get("data", "")
        return data_field
    else:
        return "Error in API response"
    
submit_button = st.button('Submit')

# Button Click
if submit_button:
    if user_input:
        data_field = send_post_request(user_input)
        st.write("Response Data:")
        st.write(data_field)
    else:
        st.error("Du måste ju skriva något...")


