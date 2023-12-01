from dotenv import load_dotenv
from constants import API_SECRET_ENV_NAME, API_CLIENT_ID_ENV_NAME
import base64
import time
import praw
import json
# from psaw import PushshiftAPI
import os
import logging
from urllib import request

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
for logger_name in ("praw", "prawcore"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

def get_comments_from_subreddit(subreddit: str, hello):
    api = os.environ['REDDIT_API_URL']
    client_id = os.environ[API_CLIENT_ID_ENV_NAME]
    client_secret = os.environ[API_SECRET_ENV_NAME]

    comments_dict = {}
    after = ''
    while True:
        time.sleep(3)
        after_param = f'&after={after}' if after != '' else ''
        req = request.Request(f'{api}/r/{subreddit}/comments/.json?limit=100&raw_json=1{after_param}')
        req.add_header("Authorization", f'Basic {client_id}:{client_secret}')
        req.add_header("User-agent", "Subreddit comment scraping bot")

        # try:
        print("Sending request")
        res = request.urlopen(req)
        # except:
        #     print("Rate limit... sleeping")
        #     time.sleep(30)
        #     continue
            # get_comments_from_subreddit(subreddit, before, True)

        j = json.loads(res.read())

        for comment in j['data']['children']:
            comment = comment['data']

            comments_dict[comment['name']] = comment['body']

        print(len(comments_dict))
        after = j['data']['after']

        # print(j['data']['children'][0]['data'].keys())
        if after == '':
            print('No more comments')
            return
        
        with open(f'datacollection/scraped/{subreddit}_{len(comments_dict)}.txt', 'w', encoding='utf-8') as f:
            f.writelines(json.dumps(comments_dict))

        # time.sleep(3)




def main():
    load_dotenv()
    get_comments_from_subreddit('techsupport', True)
    # api = PushshiftAPI()

    # api.search_comments(subreddit="relationship_advice")

    # client_id = os.environ[API_CLIENT_ID_ENV_NAME]
    # client_secret = os.environ[API_SECRET_ENV_NAME]
    # reddit = praw.Reddit(client_id= client_id, client_secret=client_secret, user_agent="testscript")
    
    # subreddit = reddit.subreddit("relationship_advice")
    
    # comment_count = 0

    # # comments = subreddit.comments.replace_more(limit=2048)
    # comments = subreddit.comments(limit=None)

    # # print(type(comments))
    # for comment in comments:
    #     # print(comment.body)
    #     comment_count += 1
    #     # time.sleep(1)
    #     # print("Comment count" omment_count)
    # print("Got: ", comment_count)
    
    # # print(reddit.read_only)

    # for submission in reddit.subreddit("relationship_advice").top():
    #     print(submission.title)

if __name__ == "__main__":
    main()
