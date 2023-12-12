import random
import keyword_extraction
from collections import deque
import pickle


class ContextTreeNode:
    def __init__(self):
        self.children = {}
        self.probabilities = {}

    def add_child(self, word):
        if word not in self.children:
            self.children[word] = ContextTreeNode()
        return self.children[word]

    def update_probability(self, word):
        if word in self.probabilities:
            self.probabilities[word] += 1
        else:
            self.probabilities[word] = 1

    def update_probability(self, word, boost_factor=1):
        if word in self.probabilities:
            self.probabilities[word] += boost_factor
        else:
            self.probabilities[word] = boost_factor

def normalize_probabilities(node):
    total = sum(node.probabilities.values())
    if total > 0:
        for word in node.probabilities:
            node.probabilities[word] /= total
    for child in node.children.values():
        normalize_probabilities(child)

def build_context_tree(comments, max_context_length=2, keyword_dict=None):
    root = ContextTreeNode()

    for comment in comments:
        for i in range(len(comment)):
            current_node = root
            for j in range(max_context_length, 0, -1):
                if i-j < 0:
                    continue
                context_word = comment[i-j]
                current_node = current_node.add_child(context_word)
            
            next_word = comment[i + 1] if i < len(comment) - 1 else '.'

            # Check if keyword_dict is provided and get the boost factor
            boost_factor = 1
            if keyword_dict is not None:
                boost_factor = keyword_dict.get(next_word, 1)

            current_node.update_probability(next_word, boost_factor)
    
    # Normalize probabilities
    normalize_probabilities(root)

    return root


def sample_next_word(current_node):
    words = list(current_node.probabilities.keys())
    probabilities = list(current_node.probabilities.values())

    # Handle the case where there are no valid probabilities
    if not probabilities or all(prob == 0 for prob in probabilities):
        return '.'  # You can return a default word or handle this case as needed

    # Randomly choose a word based on the probability distribution
    next_word = random.choices(words, weights=probabilities, k=1)[0]
    return next_word



def random_walk_vlmc(root, iterations, max_context_length):
    current_node = root
    context = deque(maxlen=max_context_length)

    for _ in range(iterations):
        if not current_node.children:
            current_node = root  # Reset to root if no children
            context.clear()

        next_word = sample_next_word(current_node)
        print(next_word, end=' ')

        if next_word == '.':
            current_node = root  # Reset to root after a period
            context.clear()
        else:
            # Update context with the next word
            context.append(next_word)

            # Navigate to the node matching the updated context
            current_node = root
            for word in context:
                current_node = current_node.children.get(word, current_node)


def main(comments=None, n = 350, max_context_length=2):


    
    root = build_context_tree(comments, max_context_length)

    # Perform a random walk on the context tree
    print('Eder intelligenta kavalier har funderat och kommit fram till följande:')
    random_walk_vlmc(root, n, max_context_length)


if __name__ == '__main__':
    main()
    
