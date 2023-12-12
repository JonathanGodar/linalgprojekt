import VLMC
from matrisförb import tokenize_comment
import re
def load_comments(file,max_words=100000):
    with open(file, 'r') as file:
        comments = []
        word_count = 0
        for line in file:
            if line.strip():
                comment = tokenize_comment(line.strip())
                comment_copy = [word for word in comment if len(word) < 15]
                word_count += len(comment_copy)
                if word_count > max_words:
                    break
                comments.append(comment_copy)

    return comments
"""
def load_comments(file_path, ignored_substrings=None):
    if ignored_substrings is None:
        ignored_substrings = []  # Default to an empty list if none provided


    def should_ignore(word):
        # Check if the word contains both letters and numbers
        if re.search(r'[a-zA-Z]', word) and re.search(r'\d', word):
            return True
        
        # Check if the word contains more than four numbers
        if len(re.findall(r'\d', word)) > 4:
            return True

        return any(substring in word for substring in ignored_substrings)


    with open(file_path, 'r') as file:
        comments = []
        for line in file:
            if line.strip():
                comment = tokenize_comment(line.strip())
                comment_copy = [word for word in comment if len(word) < 13 and not should_ignore(word)]
                comments.append(comment_copy)

    return comments"""


def main():
  #  igstrings="""http 062021 uzjz tlt gld tza si xlu dtc didis td ntnx comawaxslmt redd chb comgalleryqncjzps"""
  #  ignored_substrings = igstrings.split()  # Example substrings to ignore
    comments = load_comments('selftexts2output.txt')
    VLMC.main(comments) 

if __name__ == '__main__':
	main()