import json
import re
import numpy as np



def tokenize_comment(comment):
    # Clean the text
    cleaned_data = re.sub(r'[^a-zA-Z\s]', '', comment).lower()

    # Split the cleaned text into words
    words = cleaned_data.split()

    return words

    # # Join the words back together with spaces
    # cleaned_text = ' '.join(words)
    # comments.append(cleaned_text)

def load_comments(file):
    print("Hello?")
    comments_json = json.load(open(file))

    comments = list(map(lambda comment: tokenize_comment(comment), comments_json.values()))
    print(comments)
    return comments



# # Assuming you have loaded your JSON data into a variable named 'data'
# # For example, if your data is in a file named 'datacomment.json', you would load it like this:
# with open('datacomment.json', 'r') as file:
#     data = json.load(file)

# comments = []

# # Loop through each comment in the data
# for comment in data['data']:

# # Tokenization and vocabulary creation
# tokens = set(word for comment in comments for word in comment.split())
# vocab = {word: i for i, word in enumerate(tokens)}

# # Initialize transition matrix
# matrix_size = len(vocab)
# transition_matrix = np.zeros((matrix_size, matrix_size))

# # Fill the transition matrix
# for comment in comments:
#     words = comment.split()
#     for i in range(len(words) - 1):
#         current_word, next_word = words[i], words[i + 1]
#         transition_matrix[vocab[current_word]][vocab[next_word]] += 1

# # Convert counts to probabilities
# transition_matrix = transition_matrix / transition_matrix.sum(axis=1, keepdims=True)


# # Now transition_matrix is your Markov chain transition matrix
# print(len(transition_matrix))
# print(len(transition_matrix[0]))
# print(transition_matrix)
# print(tokens)
# print(len(tokens))
# amt=0
# for row in transition_matrix:
#     for col in row:
#         if col>0:
#             amt+=1
# print(amt)