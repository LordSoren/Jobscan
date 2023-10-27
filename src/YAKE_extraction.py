from yake import KeywordExtractor

def YAKE_keyword_extraction(text):
    extractor = KeywordExtractor(lan="en", top=10)  # Adjust the number of keywords as needed
    keywords = extractor.extract_keywords(text)
    results = {keyword[0].lower() for keyword in keywords}
    return results
