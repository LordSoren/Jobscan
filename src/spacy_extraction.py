import spacy
import pytextrank

def spacy_keyword_extraction(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    keywords = set([token.text.lower() for token in doc if not token.is_stop])
    return keywords

def pyTextRank_keyword_extraction(text):
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("textrank")

    doc = nlp(text)
    # Get the key phrases
    keyphrases = set([phrase.text.lower() for phrase in doc._.phrases])
    return keyphrases
