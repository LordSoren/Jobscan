from yake import KeywordExtractor

def yake_keyword_extraction(text):
    extractor = KeywordExtractor(lan="en", top=10)  # Adjust the number of keywords as needed
    keywords = extractor.extract_keywords(text)
    return [keyword for keyword, _ in keywords]
