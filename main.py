import threading
import time
import datetime
from commands import command
import asyncio


def main():
    done = False
    print('|| https://github.com/zauroff ||')
    print('|| IBKR Regression Trading Bot | Start command with "/". Type /help for commands list.')
    
        
    while not done:
        prompt = input('|')
        done = True if prompt == '/quit' else command(prompt)
        
main()
