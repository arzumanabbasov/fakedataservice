import csv
import pandas as pd
import streamlit as st
from faker import Faker
from io import BytesIO

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
    st.write(pd.DataFrame(data).head())

    # create a download link for the generated data
    
     with open(file_name, 'w', newline='', encoding='utf-8') as file:
        output = BytesIO()
        writer = csv.writer(file)
        writer.writerow(selected_providers)
        writer.writerows(zip(*data))
        output.seek(0)
        st.download_button(label='Download CSV', data=output, file_name=file_name, mime='text/csv')


if __name__ == "__main__":
    main()
