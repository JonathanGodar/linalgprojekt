import numpy as np
import random

comments = [['hej', 'jag', 'heter','Maximilian', ',', 'och', 'jag', 'är', 'poetisk'], ['poesi', 'är', 'poetiskt'], ['Jag', 'är', 'något', 'jag', 'är']] # 2d array of tokens
for comment in comments:
    if comment[-1] != '.':
        comment.append('.')
    if comment[0] != '.':
        comment.insert(0, '.')



tokens = list(set(word for comment in comments for word in comment))
vocab = {word: i for i, word in enumerate(tokens)}

# Initialize transition matrix
matrix_size = len(tokens)
transition_matrix = np.zeros((matrix_size, matrix_size))

# Fill the transition matrix
for comment in comments:
    words = comment
    for i in range(len(words) - 1):
        curr_word, next_word = words[i], words[i + 1]
        transition_matrix[vocab[next_word]][vocab[curr_word]] += 1

# Convert counts to probabilities
transition_matrix = transition_matrix / transition_matrix.sum(axis=0, keepdims=True)



def sample_next_word(transition_matrix, curr_word):
    curr_column = transition_matrix[:, vocab[curr_word]]
    next_word = random.choices(tokens, weights = curr_column)[0]
    return next_word
        

def random_walk(transition_matrix, n):
    curr_word = sample_next_word(transition_matrix, '.')
    print(curr_word[0].upper() + curr_word[1:], end = '')
    i = 0
    while i < n or curr_word != '.':
        last_word = curr_word
        curr_word = sample_next_word(transition_matrix, curr_word)
        if curr_word != '.' and last_word != '.':
            print(' ' + curr_word, end = '')
        elif curr_word != '.':
            upper_curr_word = curr_word[0].upper() + curr_word[1:]
            print(' ' + upper_curr_word, end = '')
        else: 
            print(curr_word, end = '')
        i += 1

random_walk(transition_matrix,  10)