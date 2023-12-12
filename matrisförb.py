import json
import re
import numpy as np



def tokenize_comment(comment):
    # Clean the text
    comment_copy = []
    curr_word = ''
    for letter in comment:
        if letter in ' ,.!?':
            if curr_word != '':
                comment_copy.append(curr_word)
                curr_word = ''
            if letter in ',.!?':
                comment_copy.append(letter)    
        else:
            if letter.isalpha() or letter.isdigit():
                curr_word += letter.lower()
    # Split the cleaned text into words
    if curr_word != '':
        comment_copy.append(curr_word)
    return comment_copy


def load_comments(file):
    
    comments_json = json.load(open(file))

    comments = list(filter(lambda comment: len(comment) != 0, map(lambda comment: tokenize_comment(comment), comments_json.values())))
    comments_copy = []
    for comment in comments:
        comment_copy = []
        for word in comment:
            if len(word) < 15:
                comment_copy.append(word)
        if comment_copy:
            comments_copy.append(comment_copy)
    return comments_copy