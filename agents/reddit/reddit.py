import praw
from langchain_ollama import ChatOllama
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
USER_AGENT = "python:travel_assistant:1.0 (by /u/atp_gamer)"

class RedditAgent:
    def __init__(self, destination) -> None:
        self.destination = destination
        self.reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_SECRET,
            user_agent=USER_AGENT
        )
        self.model = ChatOllama(model="llama3.2")
    
    # Function to fetch top posts from a subreddit
    def fetch_top_posts_in_sub(self, subreddit_name, query, limit):
        urls = []
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            results = subreddit.search(query, sort="relevance", time_filter="year", limit=limit)
            print(f"Top {limit} search results for '{query}' in r/{subreddit_name}:\n")
            for idx, post in enumerate(results, start=1):
                urls.append(post.url)
                print(f"{idx}. {post.title} (Score: {post.score})")
                print(f"   URL: {post.url}\n")

        except Exception as e:
            print(f"An error occurred: {e}")
        
        return urls

    def get_subreddits_relevant_for_query(self, query, limit) -> list:
        prompt =f"""
        Find the top {limit} most relevant subreddits based on the query below. Return a comma separated list and nothing else.
        {query}
        """
        model_output = self.model.invoke(prompt)
        return [sub.split('r/')[-1] for sub in model_output.content.split(",")] 


    def fetch_top_posts_for_query(self, query, limit):
        subreddit_list = self.get_subreddits_relevant_for_query(query, limit)
        top_posts_in_sub = {}
        for sub in subreddit_list:
            top_posts_in_sub[sub] = self.fetch_top_posts_in_sub(sub, query, limit)
        return top_posts_in_sub
    
    def fetch_post_content_and_comments(self, post_url, comment_limit=5):
        try:
            # Get the submission object
            submission = self.reddit.submission(url=post_url)

            # Fetch title and main body of the post
            title = submission.title
            main_body = submission.selftext  # This will be empty if it's a link post

            # Prepare the string to store all content
            combined_content = f"Title: {title}\n\nMain Body:\n{main_body}\n\nTop {comment_limit} Comments:\n"

            # Sort comments by top
            submission.comment_sort = "top"
            submission.comments.replace_more(limit=0)  # Load all comments

            # Add top comments to the combined content
            for idx, comment in enumerate(submission.comments[:comment_limit], start=1):
                combined_content += f"{idx}. {comment.body}\n\n"

            return combined_content

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def construct_query(self):
        return f"Things to do in {self.destination} for a tourist"

    
    def generate_recommendations(self):
        query = self.construct_query()
        limit = 5
        top_posts = self.fetch_top_posts_for_query(query, limit)
        doc_list = []
        for sub in top_posts:
            for url in top_posts[sub]:
                submission = self.fetch_post_content_and_comments(url)
                doc_list.append(submission)

        prompt = f"""
        Using the content below fetched from multiple subreddits on {self.destination} travel, provide recommendations on things to do in Greece.
        Do not generate responses for the questions that may be present in the content and ignore anything irrelevant for tourists. 
        Your only job is to generate recomendations for tourists.
        Content: 
        {', '.join(doc_list)}
        """
        return self.model.invoke(prompt)




destination = "greece"
reddit_agent = RedditAgent(destination)
recs = reddit_agent.generate_recommendations()
print(recs)