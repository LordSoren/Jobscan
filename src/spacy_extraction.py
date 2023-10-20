import spacy

nlp = spacy.load("en_core_web_sm")

def spacy_keyword_extraction(text):
    doc = nlp(text)
    keywords = [token.text for token in doc if not token.is_stop]
    return keywords