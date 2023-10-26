import spacy
import pyTextRank



def spacy_keyword_extraction(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    keywords = set([token.text for token in doc if not token.is_stop])
    return keywords

def pyTextRank_keyword_extraction(text):
    nlp = spacy.load("en_core_web_sm")
    tr = pyTextRank.TextRank()
    nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)

    text = "Your input text goes here."
    doc = nlp(text)

    # Get the key phrases
    keyphrases = set([phrase for phrase, score in doc._.phrases])
    return keyphrases
