import json
import re
import numpy as np



def tokenize_comment(comment):
    '''function that makes the comment have the right format: a list of all the words and punctuation marks.'''
    
    #create an empty copy of the comment
    comment_copy = []
    curr_word = ''
    for letter in comment:
        #continue adding letters to the word until we reach a punctuation mark or space.
        if letter in ' ,.!?':
            if curr_word != '':
                comment_copy.append(curr_word)
                curr_word = ''
            if letter in ',.!?':
                comment_copy.append(letter) 
        else:
            #check that we have a number or letter
            if letter.isalpha() or letter.isdigit():
                curr_word += letter.lower()
    if curr_word != '':
        comment_copy.append(curr_word)
    return comment_copy


def load_comments(file):
    '''function that reads the comments. Returns a list of lists, the inner lists containing words from a single comment.'''
    comments_json = json.load(open(file))

    comments = list(filter(lambda comment: len(comment) != 0, map(lambda comment: tokenize_comment(comment), comments_json.values())))
    
    #create a copy of the comments
    comments_copy = []
    
    #remove too long words, since they are probably links.
    for comment in comments:
        comment_copy = []
        for word in comment:
            if len(word) < 15:
                comment_copy.append(word)
        if comment_copy:
            comments_copy.append(comment_copy)
    return comments_copy