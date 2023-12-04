from rake_nltk import Rake


def keyword_extraction(prompt):
    r = Rake()

    # Extraction given the text.
    r.extract_keywords_from_text(prompt)

    # To get keyword phrases ranked highest to lowest with scores.
    keywords = r.get_ranked_phrases_with_scores()
    
    keyword_dict = {keyword[1]: keyword[0] for keyword in keywords}
    keys = list(keyword_dict.keys())
    for key in keys:
        key_split = key.split()
        if len(key_split) > 1:
            for single_word_keyword in key_split:
                keyword_dict[single_word_keyword] = keyword_dict[key]
            keyword_dict.pop(key)
    return keyword_dict
