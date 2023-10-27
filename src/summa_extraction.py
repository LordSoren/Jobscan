from summa import keywords

def summa_keyword_extraction(text):
    keywords_text = keywords.keywords(text)
    results = keywords_text.split("\n")
    results = {result.lower() for result in results}
    return results
