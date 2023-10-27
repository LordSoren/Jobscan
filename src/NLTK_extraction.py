import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

nltk.download("stopwords")

"""
This is actually just bad.

TODO: Fix this.
"""

def nltk_keyword_extraction(text):
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalpha()]
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words]
    fdist = FreqDist(words)
    keywords = fdist.most_common(40)  # Arbitrarily chose 40 because that's twice what Jobscan gives.
    #return results as a set of words lowercase
    return {word[0].lower() for word in keywords}
