import requests
import json
from urllib.parse import quote
import pandas as pd
from datetime import datetime
import streamlit as st

org_id = "1524030"
access_token = "AQV5pi5X2CBPhSGGSxzBHuVHcu6__kjAHQqSGM1K0sQs1hBfg_5cW3jTPHf0px9iBDX_kPp-AqQGK8BoCKASNYWc3lAd0mJfouKA8IzT3ux265k9yjHBNlQ4WJhW1Qr5zFGBHMpGloXFsQuok1yQa_i3s5EvMW9rM4_jyy4Zq_Urynn9eyoke7BCuq0qWKWR5AvSC0tD0j4EXrJMrkXWfwV0aC4mQdTXuuGnynAarkuNnE086imJC_hj8qxeda-6o_YeB8r6qq0873kHswXwxNta3cUNje0HhCIw3fUSupYR92kRFvY0Jxr24pcvKqrQHJbNXvRP_VUenjHS3HVTVqGnelkcJg"  # Replace with yours
org_urn = f"urn:li:organization:{org_id}"
org_urn_encoded = quote(org_urn)

headers = {
    "Authorization": f"Bearer {access_token}",
    "X-Restli-Protocol-Version": "2.0.0",
    "LinkedIn-Version": "202507",
    "Content-Type": "application/json"
}

# Get total number of Impressions
# url = f"https://api.linkedin.com/rest/organizationalEntityShareStatistics?q=organizationalEntity&organizationalEntity={org_urn_encoded}"

# Time start to End and the impressions each day
url = f'https://api.linkedin.com/rest/organizationalEntityShareStatistics?q=organizationalEntity&organizationalEntity=urn%3Ali%3Aorganization%3A1524030&timeIntervals=(timeRange:(start:1751328000000,end:1753833600000),timeGranularityType:DAY)'



response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("No errors")
else:
    print(f"Error: {response.status_code} - {response.text}")

daily_stats = []
for entry in response.json()['elements']:
    date = datetime.utcfromtimestamp(entry["timeRange"]["start"] / 1000).strftime('%Y-%m-%d')
    stats = entry["totalShareStatistics"]
    daily_stats.append({
        "Date": date,
        "Unique Impressions": stats["uniqueImpressionsCount"],
        "Total Impressions": stats["impressionCount"],
        "Clicks": stats["clickCount"],
        "Likes": stats["likeCount"],
        "Comments": stats["commentCount"],
        "Shares": stats["shareCount"],
        "Engagement Rate": stats["engagement"]
    })

# Create DataFrame
daily_df = pd.DataFrame(daily_stats)
print(daily_df)
st.dataframe(daily_df)
