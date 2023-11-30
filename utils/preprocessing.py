import re

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from utils.utils import compose


def load_resources():
    nltk.download("stopwords")
    nltk.download("punkt")


en_stop_words = set(stopwords.words('english'))


def remove_extra_whitespaces(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def to_lower(text: str) -> str:
    return text.lower()


def remove_special_characters(text: str) -> str:
    # Removes special characters and punctuations
    return re.sub(r'[^\w\s]', '', text)


def remove_stopwords(text: str) -> str:
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in en_stop_words]
    return " ".join(filtered_text)


def composed_preprocessing_functions():
    composed = compose(remove_extra_whitespaces, to_lower, remove_special_characters, remove_stopwords)
    return composed
