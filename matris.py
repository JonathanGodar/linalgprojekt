import json

# Assuming you have loaded your JSON data into a variable named 'data'
# For example, if your data is in a file named 'data.json', you would load it like this:
with open('datacomment.json', 'r') as file:
    data = json.load(file)

comments = []
# Loop through each comment in the data
i=0
for comment in data['data']:
    # Access the text in the 'body' field
    body_text = comment['body']
    comments.append(body_text)
    i+=1

    # You can perform additional processing here as needed
print(i)

import numpy as np

# Example comments


# Tokenization and vocabulary creation
tokens = set(word for comment in comments for word in comment.split())
vocab = {word: i for i, word in enumerate(tokens)}

# Initialize transition matrix
matrix_size = len(vocab)
transition_matrix = np.zeros((matrix_size, matrix_size))

# Fill the transition matrix
for comment in comments:
    words = comment.split()
    for i in range(len(words) - 1):
        current_word, next_word = words[i], words[i + 1]
        transition_matrix[vocab[current_word]][vocab[next_word]] += 1

# Convert counts to probabilities
transition_matrix = transition_matrix / transition_matrix.sum(axis=1, keepdims=True)

# Now transition_matrix is your Markov chain transition matrix
print(len(transition_matrix))
print(len(transition_matrix[0]))
print(transition_matrix)
print(words)
print(len(words))