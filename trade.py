import os
from ib_insync import *
from regression import *
from screener import *
import asyncio
import threading
warnings.simplefilter(action='ignore', category=DeprecationWarning)
warnings.simplefilter(action='ignore', category=ModuleNotFoundError)

ib = IB()
def clear():
    os.system('cls||clear')

def connect():
    try:
        ib.connect('127.0.0.1', 7497, clientId=2)
        clear()
        print('|| Connected to IBKR')
        ib.sleep(5)
        
    except:
        print("Connection Error. Open IBKR Workstation")

connect() # connect as soon as program starts


    
def portfolio():
    positions = ib.positions()
    positions_list = []
    for position in positions:
        positions_list.append([str(position.contract.symbol), position.avgCost, position.position])
    return positions_list


def cash_balance():
    value  = [v for v in ib.accountValues() if v.tag == 'NetLiquidationByCurrency' and v.currency == 'BASE']
    value = value[0].value
    return float(value)

def place_order(action, ticker, quantity):
    action = action.upper()
    contract = Stock(ticker, 'SMART', 'USD')
    ib.qualifyContracts(contract)
    order = MarketOrder(action, quantity)
    ib.placeOrder(contract, order)
    print(f'|| {action}: {ticker} , {quantity} shares')


def auto_trade():
    ticker_list = master_screen()
    quantity = 5
    positions = []
    buy_list = []
    
    for position in portfolio():
        positions.append(position[0])
    
    
    for ticker in ticker_list:
        result = regres(ticker, False)
        action = result[1]
        if action == 'Buy':
            buy_list.append(ticker)
            
    for ticker in buy_list:
        if ticker not in positions:
            place_order('Buy', ticker, quantity)
            
    for position in portfolio():
        ticker = position[0]
        avg_price = position[1]
        position_quantity = position[2]
        market_price = yf.Ticker(ticker).history(period='1d')['Close'][0].round(2)
        
        if market_price > avg_price:
            action = 'Sell'
            place_order(action, ticker, position_quantity)
        
    
    
    print('Refreshing in 5 MIN')
    time.sleep(300)
            



def auto_trigger():
    print("|| Auto Trade Running. Press CTRL + C to Stop")
    try:
        while True:
            auto_trade()

    except KeyboardInterrupt:
        pass


