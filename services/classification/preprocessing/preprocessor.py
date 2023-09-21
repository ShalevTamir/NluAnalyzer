import string

import nltk
from nltk import word_tokenize, SnowballStemmer
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')
def preprocess_text(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [token.lower() for token in tokens if token.isalpha() and token.lower() not in stop_words]
    stemmer = SnowballStemmer("english")
    stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]
    return " ".join(stemmed_tokens)


def preprocess_sentence(sentence: str):
    # remove punctuation marks
    words_in_sentence = word_tokenize(sentence)
    sentence = " ".join([word for word in words_in_sentence if word != '.'])
    chars_to_exclude = ['-', '.']
    return sentence.translate({ord(character): None
                               for character in string.punctuation
                               if character not in chars_to_exclude})
