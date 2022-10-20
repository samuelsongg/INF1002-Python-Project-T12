import streamlit as st
import pandas as pd
import datetime

from assets.process_data import *

# Convert Date and Time to a more readable format
def convert_date(relative):
    today = datetime.datetime.today()
    if "days" in relative:
        delta = datetime.timedelta(days = int(relative[:relative.find(" ")]))
    elif "weeks" in relative:
        delta = datetime.timedelta(days = int(relative[:relative.find(" ")]) * 7)
    else:
        delta = datetime.timedelta(days = 0)

    posted = today - delta
    return posted.strftime("%d/%m/%Y")

# Replace "Nil" values with NA in the Applicants columns and drop any rows with "Nil" values
def clean_data(data):
    data["Job Desc"] = data["Job Desc"].apply(cleaner)
    data["Job Posted Date"] = data["Job Posted Date"].apply(convert_date)

    data["Applicants"] = data["Applicants"].replace({"Nil": None})

    nils = (data == "Nil").any(axis = 1)
    return data.drop(data[nils].index)

# Get the filters from the sidebar
def get_filters(data):
    st.sidebar.write("Data Filters")

    num_rows = data.shape[0]
    categorical_filters = pd.Series([True for _ in range(num_rows)])
    for i, column in enumerate([
        "Company Name", "Sector", "Employment Type",
        "Position Level", "Work Type",
    ]):
        filter_ = st.sidebar.multiselect(
            label = column,
            options = data[column].unique(),
            default = []
        )

        if filter_ != []:
            condition = data[column].isin(filter_)
        else:
            condition = data[column].astype(bool)
        categorical_filters = categorical_filters & condition
        
    return data[categorical_filters]