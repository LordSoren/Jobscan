import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

nltk.download("stopwords")

def nltk_keyword_extraction(text):
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalpha()]
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words]
    fdist = FreqDist(words)
    keywords = fdist.most_common(10)  # Adjust the number of keywords as needed
    return [word for word, _ in keywords]
