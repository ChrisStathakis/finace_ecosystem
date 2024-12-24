from nltk.corpus import names
from nltk.stem import WordNetLemmatizer


lemmatizer = WordNetLemmatizer()
all_names = set(set(names.words()))


def is_letter_only(word):
    for char in word:
        if not char.isalpha():
            return False

    return True


def clean_text(docs):
    docs_cleaned = []
    for doc in docs:
        doc = doc.lower()
        doc_cleaned = " ".join(lemmatizer.lemmatize(word) for word in doc.split()
                                if is_letter_only(word)
                                and word not in all_names
                                )
        docs_cleaned.append(doc_cleaned)

    return docs_cleaned