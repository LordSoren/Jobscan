from summa import keywords

def pytextrank_keyword_extraction(text):
    keywords_text = keywords.keywords(text)
    return keywords_text.split("\n")
