import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import datetime as dt


def regres(ticker, plot_value):
    ticker = ticker.upper()
    start = dt.datetime.now() - dt.timedelta(1200)
    end = dt.datetime.now()
    data = yf.download(ticker, start, end) #getting stock data for ticker
    data['S_3'] = data['Close'].shift(1).rolling(window=3).mean() # 3 day moving average
    data['S_9'] = data['Close'].shift(1).rolling(window=9).mean() # 9 day moving average
    
    clean_data = data.filter(['Close','S_3','S_9'], axis=1) # filtering out moving averages and 'Close' data
    clean_data = clean_data.dropna() # removing null values
    
    
    x = clean_data[['S_3','S_9']] # x variable raw
    y = clean_data['Close'] # y variable raw
    
    t = .9 # percentage of data used for model training
    t = int(t * len(x))
    x_train = x[:t] # training x value
    y_train = y[:t] # training y value
    x_test = x[t:]  # testing x value
    y_test = y[t:]  # testing y value

    if len(x_train) != len(y_train): # debugging
        print('X and Y are not matching length!')

    linear = LinearRegression().fit(x_train, y_train) # using data to get regression
    
    pred_price = linear.predict(x_test)
    pred_price = pd.DataFrame(pred_price,index=y_test.index,columns = ['price']) # predicting price for current day    
    
    regression_price = pred_price['price'].iloc[-1].round(2)
    current_price = data['Close'].iloc[-1].round(2)
    
    if current_price < regression_price: # analysis
        result = 'Buy'
    else:
        result = 'Sell'

    def plot(plot_value):
        if plot_value == True:
            pred_price.plot(figsize=(5,5))
            y_test.plot()
            plt.legend(['Predicted Price', 'Actual Price'])
            plt.show()
            plt.title(ticker)
    plot(plot_value)
    
    r2_score = (linear.score(x[t:],y[t:])*100) # getting score for accuracy
    r2_score = "{0:.0f}%".format(r2_score)
    
    return [ticker, result, r2_score]


