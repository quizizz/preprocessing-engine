import re


PATTERNS = {
    "educational_code": re.compile(r'\d+\.[A-Z]+\.\d+'),
    "lesson_title": re.compile(r'[a-zA-Z\s]+:'),
}
