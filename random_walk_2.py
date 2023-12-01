import numpy as np
import random
import nltk
#nltk.download('averaged_perceptron_tagger')
punct = '.,!?'


def read_text(comments):
    #we will have to add a part that reads an input file here
    for comment in comments:
        if comment[-1] not in punct:
            comment.append('.')
        if comment[0] not in punct:
            comment.insert(0, '.')
    return comments


def word_check(word1, word2):
    '''checks if words are compatible'''
    try:
        w1 = nltk.pos_tag([word1])[0][1]
        w2 = nltk.pos_tag([word2])[0][1]
        if (w1 == 'JJ' and w2 == 'NN') or (w1 == 'JJ' and w2 == 'JJ') or (w1 == 'PRP' and w2 == 'VB') or (w1 == 'DT' and w2 == 'NN'):
            return True
        return False
    except:
        return False

def init_matrix(tokens, vocab, comments):
# Initialize transition matrix

    matrix_size = len(tokens)
    transition_matrix = np.zeros((matrix_size, matrix_size))

# Fill the transition matrix
    for comment in comments:
        for i in range(len(comment) - 1):
            curr_word, next_word = comment[i], comment[i + 1]
            if word_check(curr_word, next_word):
                transition_matrix[vocab[next_word]][vocab[curr_word]] += 3
            transition_matrix[vocab[next_word]][vocab[curr_word]] += 1

# Convert counts to probabilities
    transition_matrix = transition_matrix / transition_matrix.sum(axis=0, keepdims=True)
    return transition_matrix


def sample_next_word(transition_matrix, curr_word, tokens, vocab):
    curr_column = transition_matrix[:, vocab[curr_word]]
    next_word = random.choices(tokens, weights = curr_column)[0]
    return next_word


def random_walk(transition_matrix, iterations, tokens, vocab):
    curr_word = sample_next_word(transition_matrix, '.', tokens, vocab)
    print(curr_word[0].upper() + curr_word[1:], end = '')
    i = 0
    while i < iterations or curr_word not in punct or curr_word == ',':
        #the following part makes the text more grammatically correct. 
        last_word = curr_word
        curr_word = sample_next_word(transition_matrix, curr_word, tokens, vocab)
        if curr_word not in punct and last_word not in punct:
            print(' ' + curr_word, end = '')
        elif curr_word not in punct:
            if last_word != ',':
                upper_curr_word = curr_word[0].upper() + curr_word[1:]
                print(' ' + upper_curr_word, end = '')
            else:
                print(' ' + curr_word, end = '')
        else: 
            print(curr_word, end = '')
        i += 1


def main():
    comments = read_text([['white', 'the'], ['white', 'mouse']]) # 2d array of tokens
    tokens = list(set(word for comment in comments for word in comment))
    vocab = {word: i for i, word in enumerate(tokens)}
    transition_matrix = init_matrix(tokens, vocab, comments)
    random_walk(transition_matrix,  10, tokens, vocab)



if __name__ == '__main__':
    main()