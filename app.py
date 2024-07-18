import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def fetch_college_details(college_name):
    url = "https://www.nirfindia.org/Rankings/2023/OverallRanking.html"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'id': 'tbl_overall'})
    
    columns = ['Name', 'City', 'State', 'Rank']
    data = []
    for row in table.find_all('tr')[1:]:
        cells = row.find_all('td')
        if len(cells) > 5:
            data.append({
                'Name': cells[1].text.strip(),
                'City': cells[7].text.strip(),
                'State': cells[8].text.strip(),
                'Rank': cells[10].text.strip(),
            })
    df = pd.DataFrame(data, columns=columns)
    college_details = df[df['Name'].str.contains(college_name, case=False, na=False)]
    
    if not college_details.empty:
        college_details['Name'] = college_name
        return college_details
    else:
        return pd.DataFrame(columns=columns)

# Streamlit UI
st.title("College Details Fetcher")

college_name = st.text_input("Enter the name of the college:")
if college_name:
    college_details = fetch_college_details(college_name)
    if not college_details.empty:
        st.write(f"Details for: {college_name}")
        st.table(college_details)
    else:
        st.write(f"College named {college_name} not found in the NIRF rankings.")
