# imports
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import yfinance as yf

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
