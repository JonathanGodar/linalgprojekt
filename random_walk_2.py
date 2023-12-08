import numpy as np
import random
import nltk
#nltk.download('averaged_perceptron_tagger')
import keyword_extraction
from collections import deque
import math
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


'''def word_check(word1, word2):
    #checks if words are compatible
    try:
        w1 = nltk.pos_tag([word1])[0][1]
        w2 = nltk.pos_tag([word2])[0][1]
        print(word1, w1, word2, w2)
        if (w1 == 'JJ' and w2 == 'NN') or (w1 == 'JJ' and w2 == 'JJ') or (w1 == 'PRP' and w2 == 'VB') or (w1 == 'DT' and w2 == 'NN'):
            return True
        return False
    except Exception as error:
        print(error)
        return False
    except Exceptionerror:
        return False'''

def init_matrix(tokens, vocab, comments, keyword_dict):
    
    # Initialize transition matrix
    matrix_size = len(tokens)
    transition_matrix = np.zeros((matrix_size, matrix_size))
    
    # Fill the transition matrix
    for comment in comments:

        #create a list with the previous words to boost all of them if a keyword is found.        
        previous_words = []
        booster = 30
        booster_decay = 0.8
        number_of_words = 20

        for i in range(len(comment) - 1):
            curr_word, next_word = comment[i], comment[i + 1]
            
            #update the list of previous words
            previous_words.insert(0, next_word)
            while len(previous_words) > number_of_words:
                previous_words.pop()
            
            #boost all the previous words if keyword is found.
            if next_word in keyword_dict:
                for i in range(len(previous_words) - 1):
                    transition_matrix[vocab[previous_words[i]]][vocab[previous_words[i+1]]] += booster * keyword_dict[next_word]
                    booster *= booster_decay
            
            #if a word is not a keyword it doesnt get a boost
            else:        
                transition_matrix[vocab[next_word]][vocab[curr_word]] += 1

# Convert counts to probabilities
    transition_matrix = transition_matrix / transition_matrix.sum(axis=0, keepdims=True)
    return transition_matrix


def sample_next_word(transition_matricies, word_consideration_window, tokens, vocab):
    curr_column = np.zeros(len(tokens))
    for step, word in enumerate(word_consideration_window):
        curr_column += transition_matricies[step][:, vocab[word]] * (math.e ** -step)

    weights = curr_column / curr_column.sum(keepdims=True)
    next_word = random.choices(tokens, weights)[0]
    return next_word

def random_walk(transition_matrix, iterations, tokens, vocab, step):
    transition_matricies = [transition_matrix]
    for _ in range(step -1):
        transition_matricies.append(transition_matricies[-1] @ transition_matrix)
    
    word_consideration_window = deque(maxlen=step)
    word_consideration_window.appendleft('.')

    curr_word = sample_next_word(transition_matricies, word_consideration_window, tokens, vocab)
    print(curr_word[0].upper() + curr_word[1:], end = '')

    i = 0
    while i < iterations or curr_word not in punct or curr_word == ',':
        #the following part makes the text more grammatically correct. 
        last_word = curr_word
        curr_word = sample_next_word(transition_matricies, word_consideration_window, tokens, vocab)
        word_consideration_window.appendleft(curr_word)

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
    pass

def main(comments, n, step = 1):
    comments = read_text(comments) # 2d array of tokens
    tokens = list(set(word for comment in comments for word in comment))
    vocab = {word: i for i, word in enumerate(tokens)}


    keyword_dict = keyword_extraction.keyword_extraction(input('Eder fråga, ädle riddare: '))
    print(f'Följande nyckelord identifierades i eder fråga: {keyword_dict}')

    print(f'Eder inteligenta betjänt har funderat och kommit fram till följande:')
    transition_matrix = init_matrix(tokens, vocab, comments, keyword_dict)
    random_walk(transition_matrix, n, tokens, vocab, step)


if __name__ == '__main__':
    main()