import pandas as pd
import numpy as np
import nltk
import re
import os

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# get raw data that was scraped from LinkedIn
def get_raw_data():

    cs = pd.read_excel("C:/Users/kenri/PycharmProjects/Web-Crawler/raw_data/CyberSecuritySpecialist.xlsx", sheet_name = 0)
    da = pd.read_excel("C:/Users/kenri/PycharmProjects/Web-Crawler/raw_data/DataAnalyst.xlsx", sheet_name = 0)
    se = pd.read_excel("C:/Users/kenri/PycharmProjects/Web-Crawler/raw_data/SoftwareEngineer.xlsx", sheet_name = 0)

    cs["Role"] = "Cyber Security Specialist"
    da["Role"] = "Data Analyst"
    se["Role"] = "Software Engineer"

    data = pd.concat([cs, da, se], axis = 0, ignore_index = True)
    return data

# clean the job description using stopwords and tokenisation
def cleaner(desc):
    stop_words = stopwords.words("english")
    stop_words.extend([
        "business", "data", "skills", "skill", 
        "team", "opportunity", "work", "experience",
        "job", "status", "applicants", "previous"
        "sexual", "orientation"
    ])
    
    cleaned = []
    for sentence in desc.split("\n"):
        if not sentence.strip(" "):
            continue

        no_unicode = re.sub(r"[^\x00-\x7F]+", "", sentence)
        no_punctuation = re.sub("[^\w\s]", " ", no_unicode)
        no_digits = re.sub("\d+", "", no_punctuation)
        tokenized = word_tokenize(no_digits)

        tagged = nltk.pos_tag(tokenized)
        skills = []
        for tag, pos in tagged:
            if pos not in ["NN", "NNS", "NNP", "JJ"]:
                continue
            if tag.lower() in stop_words:
                continue

            skills.append(tag)
        cleaned.extend(skills)

    return " ".join(cleaned)

# Clean the raw data to get the cleaned data for analysis
def get_model_data(data):
    cleaned_desc = data["Job Desc"].apply(cleaner)
    model_data = pd.DataFrame({"Desc": cleaned_desc, "Role": data["Role"]})
# Edit here to point to the correct path for cleaned_data.csv
    model_data.to_csv("C:/Users/kenri/PycharmProjects/Web-Crawler/cleaned_data.csv", index = False)
    return model_data