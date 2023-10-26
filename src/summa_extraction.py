from summa import keywords

def summa_keyword_extraction(text):
    keywords_text = keywords.keywords(text)
    return set(keywords_text.split("\n"))
