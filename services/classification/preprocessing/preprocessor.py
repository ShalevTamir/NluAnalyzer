import string
from nltk import word_tokenize, WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords

__lemmatizer = WordNetLemmatizer()


def preprocess_adjective(adjective: str):
    return __lemmatizer.lemmatize(adjective, pos='a')


def preprocess_sentence(sentence: str):
    sentence = sentence.lower()
    tokens = word_tokenize(sentence)
    stop_words = set(stopwords.words("english"))
    # remove stop words
    filtered_tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
    stemmer = PorterStemmer()
    # stem tokens
    stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]
    return " ".join(stemmed_tokens)


def remove_punctuation_marks(sentence: str) -> str:
    sentence = sentence[:len(sentence)-1] if sentence[len(sentence)-1] == '.' else sentence
    chars_to_exclude = ['-', '.', '\'']
    return sentence.translate({ord(character): None
                               for character in string.punctuation
                               if character not in chars_to_exclude})
