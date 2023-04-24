import csv
import pandas as pd
import streamlit as st
from faker import Faker

fake = Faker('az_AZ')


def generate_fake_data(selected_providers, num_rows):
    data = []

    # generate the data for each provider
    for provider in selected_providers:
        provider_func = getattr(fake, provider)
        column_data = [provider.capitalize()]
        for _ in range(num_rows):
            column_data.append(provider_func())
        data.append(column_data)

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
    file_name = st.text_input('Enter file name', value='fake_data.csv')

    # generate the fake data
    data = generate_fake_data(selected_providers, num_rows)

    # display the demo table
    st.write('## Demo Table')
    st.write(pd.DataFrame(data).T.head(5))

    # create a download link for the generated data
    if st.button('Download'):
        with open(file_name, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(selected_providers)
            writer.writerows(zip(*data))
            st.download_button(label='Download CSV', data=output, file_name='fake_data.csv', mime='text/csv')
        st.success(f'Downloaded {file_name} with {num_rows} rows and {len(selected_providers)} columns.')


if __name__ == "__main__":
    main()
