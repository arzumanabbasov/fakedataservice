import csv
import pandas as pd
import streamlit as st
from faker import Faker
from io import BytesIO
import base64

fake = Faker('az_AZ')


def generate_fake_data(selected_providers, num_rows):
    data = []

    # generate the data for each row
    for _ in range(num_rows):
        row = []
        for provider in selected_providers:
            provider_func = getattr(fake, provider)
            row.append(provider_func())
        data.append(row)

    return data


def main():
    st.title('Fake Data Generator')
    st.sidebar.title('Column Selection')
    all_providers = dir(fake)

    # define the available providers
    available_providers = [p for p in all_providers if not p.startswith('_')]

    # create checkboxes for provider selection
    selected_providers = st.sidebar.multiselect('Select Columns', available_providers)

    # get the number of rows from the user
    num_rows = st.sidebar.number_input('Number of rows', value=10, min_value=1, max_value=10000)

    # get the file name from the user
    filename = st.text_input('Enter file name', value='fake_data.csv')

    # generate the fake data
    data = generate_fake_data(selected_providers, num_rows)

    # display the demo table
    st.write('## Demo Table')
    df = pd.DataFrame(data)
    st.write(df.head())
    if st.button("Download"):
        progress_bar = st.progress(0)
        for i in range(1000):
            progress_bar.progress(i+1)
        progress_bar.empty()
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)
        

if __name__ == "__main__":
    main()
