import praw
import json

class Reddit:

    def __init__(self):
        json_data = self.getKeys()

        self.reddit = praw.Reddit(
        client_id=json_data['reddit_client_id'],
        client_secret=json_data['reddit_client_secret'],
        user_agent='MyRedditApp/1.0',
        check_for_async=False
    )

    def getKeys(self):
        with open('secrets.json') as file:
            # Load the JSON data
            data = json.load(file)

        return data
    
    # Initialize the Reddit API client
    

    def getCustomPost(self, url):
        post = self.reddit.submission(url=url)
        return self.getPostAndComments(post)


    def getSubreddit(self, subreddit):

        subreddit = self.reddit.subreddit(subreddit)
        hottest_post = subreddit.hot(limit=1)
        for post in hottest_post:
            return self.getPostAndComments(post)


    def getPostAndComments(self, post):

        post_title = post.title

        # Get the top 15 threads based on the top comment
        threads = []
        for comment in post.comments:
            if comment.score > 0:
                if comment.body != '[deleted]' and comment.body != '[removed]':
                    thread = comment.body
                    threads.append(thread)
                    if len(threads) == 15:
                        break
    
        return post_title, threads
