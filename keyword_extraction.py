from rake_nltk import Rake


def keyword_extraction(prompt):
    '''function that extracts keywords from the input'''
    r = Rake()

    # Extraction given the text.
    r.extract_keywords_from_text(prompt)

    # To get keyword phrases ranked highest to lowest with scores.
    keywords = r.get_ranked_phrases_with_scores()
    
    #create dictionary with the keywords and their corresponding scores.
    keyword_dict = {keyword[1]: keyword[0] for keyword in keywords}
    
    #we split up multiple word keywords into single word keywords. All the single word keywords get the same score as the multiple word keyword. 
    keys = list(keyword_dict.keys())
    for key in keys:
        key_split = key.split()
        if len(key_split) > 1:
            for single_word_keyword in key_split:
                keyword_dict[single_word_keyword] = keyword_dict[key]
            keyword_dict.pop(key)
    return keyword_dict
