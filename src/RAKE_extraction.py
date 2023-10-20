from rake_nltk import Rake

r = Rake()

def rake_keyword_extraction(text):
    r.extract_keywords_from_text(text)
    keywords = r.get_ranked_phrases()
    return keywords
