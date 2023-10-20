from keybert import KeyBERT

model = KeyBERT()

def keybert_keyword_extraction(text):
    keywords = model.extract_keywords(text, stop_words="english")
    return [keyword[0] for keyword in keywords]
