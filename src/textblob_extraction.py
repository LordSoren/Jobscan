from textblob import TextBlob

def textblob_keyword_extraction(text):
    blob = TextBlob(text)
    keywords = blob.noun_phrases
    keywords = {keyword.lower() for keyword in keywords}
    return keywords
