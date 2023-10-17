import string
from nltk import word_tokenize, WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords
from spacy.tokens import Token


def preprocess_token(token: Token):
    return token.lemma_


def preprocess_sentence(sentence: str):
    sentence = sentence.lower()
    tokens = word_tokenize(sentence)
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return " ".join(stemmed_tokens)


def remove_punctuation_marks(sentence: str) -> str:
    sentence = sentence[:len(sentence)-1] if sentence[len(sentence)-1] == '.' else sentence
    chars_to_exclude = ['-', '.', '\'', '_']
    return sentence.translate({ord(character): None
                               for character in string.punctuation
                               if character not in chars_to_exclude})
