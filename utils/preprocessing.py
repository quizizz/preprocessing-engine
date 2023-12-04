import re

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from utils.utils import compose
from utils.regex_store import PATTERNS
from nltk.stem import WordNetLemmatizer


def load_resources():
    nltk.download("stopwords")
    nltk.download("punkt")
    nltk.download('wordnet')


en_stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def remove_extra_whitespaces(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def to_lower(text: str) -> str:
    return text.lower()


def remove_special_characters(text: str) -> str:
    # Removes special characters and punctuations except '.', '=', '+', and '-'
    return re.sub(r'[^\w\s.=+-]', '', text)


def remove_stopwords(text: str) -> str:
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in en_stop_words]
    return " ".join(filtered_text)


def lemmatize(text: str) -> str:
    return " ".join([lemmatizer.lemmatize(word) for word in word_tokenize(text)])


PROCESSING_FUNCTIONS = {
    'educational_code': compose(remove_extra_whitespaces, remove_special_characters),
    'lesson_title': compose(remove_extra_whitespaces, to_lower, remove_special_characters),
    'general': compose(remove_extra_whitespaces, to_lower, remove_special_characters, remove_stopwords),
    'general_lemmatize': compose(
        remove_extra_whitespaces, to_lower, remove_special_characters, remove_stopwords, lemmatize
    )
}


def composed_preprocessing_function(processing_function=None):
    def classify_query(text: str) -> str:
        for query_type, pattern in PATTERNS.items():
            if pattern.match(text):
                return query_type
        return processing_function or "general"

    return lambda text: PROCESSING_FUNCTIONS[classify_query(text)](text)
