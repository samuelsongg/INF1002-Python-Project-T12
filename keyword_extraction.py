import nltk
nltk.download("punkt")
nltk.download("stopwords")
import RAKE
import os
from rake_nltk import Rake

# def extract_keyword():
#     r = Rake()
#     r.extract_keywords_from_text(text_body)
#     print(r.get_ranked_phrases_with_scores())
#     for rating, keyword in r.get_ranked_phrases_with_scores():
#         if rating > 5:
#             print(rating, keyword)

def extract_text():
    with open("bodytext.txt", "r") as f:
        return f.read()

r = Rake()
r.extract_keywords_from_text(extract_text())
for rating, keyword in r.get_ranked_phrases_with_scores():
    if rating > 5:
        print(rating, keyword)
