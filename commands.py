import threading
from trade import *
from screener import *
from regression import *
import matplotlib.pyplot
warnings.simplefilter(action='ignore', category=UserWarning)

def command(prompt):
    if prompt.startswith('/',0):
            command = prompt[1:]
            match command:
                case "connected":
                    print(ib.isConnected())
                case "portfolio":
                    print(portfolio())
                case "regression chart":
                    userTicker = input('|| Enter Ticker: ')
                    regres(userTicker, True)
                    matplotlib.pyplot.close("all")
                case "regression detailed":
                    userTicker = input('|| Enter Ticker: ')
                    print(regres(userTicker, False))
                case "run":
                    auto_trigger()
                case "help":
                    print({
                        "/Connected : Check to see if you are connected to IBKR",
                        "/Portfolio : See current positions",
                        "/Regression (chart, detailed) : View details on linear regression",
                        "/Run : Run the Auto Trade"
                    })
                    
                    
                    
                    
                case other:
                    print('|| Invalid Command. Type /help for commands list.')
                

    
