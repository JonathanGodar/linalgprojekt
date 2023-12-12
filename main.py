from matrisförb import load_comments
import random_walk_2

def main():
	comments = load_comments('datacollection/scraped/techsupport_931.txt')
	random_walk_2.main(comments, 25, 10) 

if __name__ == '__main__':
	main()