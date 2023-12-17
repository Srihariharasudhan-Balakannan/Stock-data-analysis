# imports
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import yfinance as yf
import praw
import pandas as pd
from praw.models import MoreComments

# get top listed companies and their symbols for nasdaq
def top_nasdaq():
    try:
        response = requests.get('https://www.fool.com/investing/stock-market/indexes/nasdaq/')
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find('ol')
        company_details = {}
        for datum in data:
            company_details[datum.find('b').text] = datum.find('a').text
        return company_details
    except Exception as e:
        return {'exception': e}

# function to get stock data 
def get_stock_data(symbol:str, yrs:int):
    end_date = str(datetime.now())[:10]
    start_date = str(datetime.now() - timedelta(days=365*yrs))[:10]
    df = yf.download(symbol, start=start_date, end=end_date)
    return df

# function that returns posts from Reddit in the form of a data frame, about a particular topic
def get_reddit_posts(query:str):
    user_agent = "praw_scraper_1.0"
    reddit = praw.Reddit(username = "< REDDIT USER NAME >",
                        password = "< REDDIT PASSWORD >",
                        client_id = "< YOUR CLIENT ID >",
                        client_secret = "< YOUR CLIENT SECRET >",
                        user_agent=user_agent
    )
    posts = []
    for post in reddit.subreddit('all').search(query):
        comments_str = ''
        for comment in post.comments:
            if isinstance(comment, MoreComments):
                continue
            comments_str = comments_str + comment.body + '\n'
        posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created, comments_str])
    df = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created', 'comments'])
    return df

