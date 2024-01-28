import praw
import time

# Set up your Reddit API credentials
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
username = 'YOUR_REDDIT_USERNAME'
password = 'YOUR_REDDIT_PASSWORD'
user_agent = 'YOUR_USER_AGENT'  # Describe your bot (e.g., 'MyAwesomeBot by /u/YourUsername')

# Authenticate with Reddit API
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    username=username,
    password=password,
    user_agent=user_agent
)

def run_bot(subreddit_name, reply_phrase, sleep_time=30, num_comments=10):
    subreddit = reddit.subreddit(subreddit_name)

    print(f"Bot is now running in /r/{subreddit_name}...\n")

    while True:
        try:
            for submission in subreddit.new(limit=num_comments):
                process_submission(submission, reply_phrase)

            print(f"Sleeping for {sleep_time} seconds...\n")
            time.sleep(sleep_time)

        except praw.exceptions.APIException as e:
            print(f"API Exception: {e}")
            print("Sleeping for 5 minutes...")
            time.sleep(300)

def process_submission(submission, reply_phrase):
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        # Check if the comment has already been replied to
        replied_to = any(
            reply.author.name == username for reply in comment.replies.list()
        )

        if not replied_to and 'python' in comment.body.lower():
            print(f"Replying to comment in thread {submission.title}...")
            comment.reply(reply_phrase)
            print("Replied!\n")

if __name__ == "__main__":
    # Example: Run the bot in the subreddit 'learnpython'
    run_bot('learnpython', 'Hello! I see you mentioned Python. I am a bot.')
