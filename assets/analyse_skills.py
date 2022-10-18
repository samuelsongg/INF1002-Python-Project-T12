import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer

# Random Forest
def run_randomforest(data, ngram = (1, 1)):
    features = data["Desc"]
    target = data["Role"]

    vectorizer = TfidfVectorizer(ngram_range = ngram)
    vectorized = vectorizer.fit_transform(features)
    feature_names = vectorizer.get_feature_names_out()

    rf = RandomForestClassifier()
    rf.fit(vectorized, target)
    
    return pd.Series(rf.feature_importances_, index = feature_names).sort_values(ascending = False)

# Multinomial Naive Bayes
def run_naivebayes(data, ngram = (2, 2)):
    features = data["Desc"]
    target = data["Role"]

    vectorizer = TfidfVectorizer(ngram_range = ngram)
    vectorized = vectorizer.fit_transform(features)
    feature_names = vectorizer.get_feature_names_out()

    nb = MultinomialNB()
    nb.fit(vectorized, target)
    
    return {name: pd.Series(feature_prob, index = feature_names) \
        for name, feature_prob in zip(nb.classes_, nb.feature_log_prob_)}

