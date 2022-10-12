import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import nltk
import os
import math

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
from functools import reduce

from assets.process_data import *
from assets.analyse_skills import *

nltk.download("wordnet")
nltk.download("omw-1.4")
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger")

stop_words = stopwords.words("english")
stop_words.extend([
    "business", "data", "skills", "skill", 
    "team", "opportunity", "work", "experience",
    "job", "status", "applicants", "previous"
])

def plot_skills(data, chosen):
    st.subheader(f"Frequency of words in {chosen} jobs")
    if chosen not in st.session_state:
        wordcloud = WordCloud(
            stopwords = stop_words,
            background_color = "white"
        ).generate_from_frequencies(data)
        st.session_state[chosen] = wordcloud
    else:
        wordcloud = st.session_state[chosen]

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.axis("off")
    cloud_plot = ax.imshow(wordcloud)
    st.pyplot(fig)

    st.subheader("Ranked Skills")

    sorted = data.nlargest(10).sort_values(ascending = False)
    num_cols = int(math.sqrt(10))
    cols = st.columns(num_cols)
    for i, value in enumerate(sorted.index):
        col = cols[(i % num_cols)]
        col.write(f"{i+1}) {value.capitalize()}")


def plot_importance(data):
    n = st.sidebar.slider(label = "Number of skills to show", min_value = 5, max_value = 20, value = 10)
    st.subheader(f"{n} most important skills across fields")
    subset = data.nlargest(n)
    st.bar_chart(subset)


def main():
    files = os.listdir()
    st.title("Explore Skills")
    if "cleaned_data.csv" not in files:
        with st.spinner("Loading Files..."):
            raw_data = get_raw_data()
            data = get_model_data(raw_data)
    else:
        data = pd.read_csv("cleaned_data.csv")

    chosen = st.sidebar.selectbox(
        label = "Choose a field", 
        options = ["Cyber Security Specialist", "Data Analyst", "Software Engineer"]
    )
    ngram = st.sidebar.slider("Choose number of words in phrase", min_value = 1, max_value = 4, value = 2)
    st.sidebar.caption("Skills makes more sense when the phrases are short (1~2)")

    with st.spinner("Running models..."):
        if f"rf{ngram}" not in st.session_state:
            rf_results = run_randomforest(data, (ngram, ngram))
            st.session_state[f"rf{ngram}"] = rf_results
        else:
            rf_results = st.session_state[f"rf{ngram}"]

        if f"nb{ngram}" not in st.session_state:
            nb_results = run_naivebayes(data, (ngram, ngram))
            st.session_state[f"nb{ngram}"] = nb_results
        else:
            nb_results = st.session_state[f"nb{ngram}"]

    plot_skills(nb_results[chosen], chosen)
    st.empty()
    plot_importance(rf_results)


if __name__ == '__main__':
    main()