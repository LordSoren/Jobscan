from yake import KeywordExtractor

def YAKE_keyword_extraction(text):
    extractor = KeywordExtractor(lan="en", top=10)  # Adjust the number of keywords as needed
    keywords = extractor.extract_keywords(text)
    return set([keyword[0] for keyword in keywords])
