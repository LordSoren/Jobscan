from rake_nltk import Rake

r = Rake()

def RAKE_keyword_extraction(text):
    r.extract_keywords_from_text(text)
    keywords = r.get_ranked_phrases()
    for keyword in keywords:
        keyword = keyword.lower()
    keywords = set(keywords)
    return keywords
