from dotenv import load_dotenv
from constants import API_SECRET_ENV_NAME, API_CLIENT_ID_ENV_NAME,REDDIT_API_URL_ENV_NAME
import time
import json
import os
import logging
from urllib import request

def get_comments_from_subreddit(subreddit: str):
    '''
    Retrieves comments from a subreddit.
    Expects the environment variables in ./constants.py to be set.
    '''

    subreddit = subreddit.lower()

	# Load env variables
    api = os.environ[REDDIT_API_URL_ENV_NAME]
    client_id = os.environ[API_CLIENT_ID_ENV_NAME]
    client_secret = os.environ[API_SECRET_ENV_NAME]

	# Dictionary containing all scraped comments(value) and their id(key) - or name as reddit calls them
    comments_dict = {}
    

	# Is the "pointer" that controls the pagination.
    after = ''
    # Go through the pagination and attempt to retrieve one page for each iteration
    while True:
        time.sleep(3) # Sleep for 3 secs to to avoid reddit API ratelimiting errors
        after_param = f'&after={after}' if after != '' else ''
        
        # Construct the request for comments from the specified subreddit
        req = request.Request(f'{api}/r/{subreddit}/comments/.json?limit=100&raw_json=1{after_param}')
        req.add_header("Authorization", f'Basic {client_id}:{client_secret}')
        req.add_header("User-agent", "Subreddit comment scraping bot")

		# Send and parse the request
        res = request.urlopen(req)
        j = json.loads(res.read())

        # Add the found comments tho the comment dict
        for comment in j['data']['children']:
            comment = comment['data']

            comments_dict[comment['name']] = comment['body']

        print(len(comments_dict))
        after = j['data']['after']

        if after == '':
            print('No more comments')
            return
        
        # Save the comments. Note this will create a separate file for each itteration of the loop 
        with open(f'datacollection/scraped/{subreddit}_{len(comments_dict)}.txt', 'w', encoding='utf-8') as f:
            f.writelines(json.dumps(comments_dict))

def main():
    """ Scrape comments from a subreddit """
    load_dotenv()
    get_comments_from_subreddit('Rhetoric')

if __name__ == "__main__":
    main()
