from yahoo_fin import stock_info as si
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import yfinance as yf
import datetime as dt
import time


blacklist = ['AMC', 'BBBY', 'BB' ,'GME']
start_time = time.time()

def active():
    tickers = si.get_day_most_active()
    tickers = tickers.iloc[:,0:1]
    tickers_array = tickers['Symbol'].tolist()
    return tickers_array
    
def snp():
    return si.tickers_sp500()


def master_screen():
    tickers_array = active()  # combine s&p and most active stocks into single array
    unfiltered_array = list(set(tuple(tickers_array))) # create set to get rid of duplicates, which is then converted into a list
    unfiltered_array.sort()
    
    filtered_array = []
    print('|| Processing')
    for ticker in unfiltered_array:
        price = yf.Ticker(ticker).history(period='1d')['Close'][0].round(2) # stock price
        if price <= 150:
            print(ticker, price)
            if ticker not in blacklist:
                filtered_array.append(ticker)
    print('|| Done Screening')
    
            
    return filtered_array
