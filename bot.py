import base64
import json
import os
import random
import sys
import time
from urllib.parse import parse_qs, unquote
from datetime import datetime, timedelta

from paws import Paws

def print_(word):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"[{now}] | {word}")


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def load_query():
    try:
        with open('paws_query.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        return queries
    except FileNotFoundError:
        print("File paws_query.txt not found.")
        return [  ]
    except Exception as e:
        print("Failed get Query :", str(e))
        return [  ]

def load_address():
    try:
        with open('address.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        return queries
    except FileNotFoundError:
        print("File address.txt not found.")
        return [  ]
    except Exception as e:
        print("Failed get Query :", str(e))
        return [  ]

def load_sol_address():
    try:
        with open('sol_address.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        return queries
    except FileNotFoundError:
        print("File address.txt not found.")
        return [  ]
    except Exception as e:
        print("Failed get Query :", str(e))
        return [  ]

def parse_query(query: str):
    parsed_query = parse_qs(query)
    parsed_query = {k: v[0] for k, v in parsed_query.items()}
    user_data = json.loads(unquote(parsed_query['user']))
    parsed_query['user'] = user_data
    return parsed_query

def print_delay(delay):
    print()
    while delay > 0:
        now = datetime.now().isoformat(" ").split(".")[0]
        hours, remainder = divmod(delay, 3600)
        minutes, seconds = divmod(remainder, 60)
        sys.stdout.write(f"\r[{now}] | Waiting Time: {round(hours)} hours, {round(minutes)} minutes, and {round(seconds)} seconds")
        sys.stdout.flush()
        time.sleep(1)
        delay -= 1
    print_("Waiting Done, Starting....\n")

def main():
    start_time = time.time()
    clear_terminal()
    queries = load_query()
    adresses = load_address()
    sum = len(queries)
    paw = Paws()
    total_balance = 0
    for index, query in enumerate(queries):
        users = parse_query(query).get('user')
        id = users.get('id')
        print_(f"[SxG]======= Account {index+1}/{sum} [ {users.get('username')} ] ========[SxG]")
        auth = paw.auth(query)
        if auth is not None:
            data = auth.get('data')
            token = data[0]
            datas = data[1]
            userData =datas.get('userData')
            wallet = userData.get('wallet',None)
            allocationData = datas.get('allocationData')
            gameData = datas.get('gameData')
            balance = gameData.get('balance')
            total_balance += balance
            total = allocationData.get('total',0)
            print_(f"Total Balance : {balance}")
            if wallet is None:
                print_('Wallet Address not found')

            else:
                print_(f"Wallet address : {wallet}")
            print_('Get Task')
            paw.quest_list(token=token)
            
    print_(f"Total {total_balance} Paws From {sum} Account")
            
def connect_ton():
    start_time = time.time()
    clear_terminal()
    queries = load_query()
    adresses = load_address()
    sum = len(queries)
    paw = Paws()
    total_balance = 0
    for index, query in enumerate(queries):
        users = parse_query(query).get('user')
        id = users.get('id')
        print_(f"[SxG]======= Account {index+1}/{sum} [ {users.get('username')} ] ========[SxG]")
        auth = paw.auth(query)
        if auth is not None:
            data = auth.get('data')
            token = data[0]
            datas = data[1]
            userData =datas.get('userData')
            wallet = userData.get('wallet',None)
            allocationData = datas.get('allocationData')
            gameData = datas.get('gameData')
            balance = gameData.get('balance')
            total_balance += balance
            total = allocationData.get('total',0)
            print_(f"Total Balance : {balance}")
            if wallet is None:
                print_('Wallet Address not found')
                address = adresses[index]
                if address is None:
                    print_('Address not found')
                else:
                    paw.bind_wallet(token=token, address=wallet)
            else:
                print_(f"Wallet address : {wallet}")

def connect_sol():
    queries = load_query()
    adresses = load_sol_address()
    sum = len(queries)
    paw = Paws()
    total_balance = 0
    for index, query in enumerate(queries):
        users = parse_query(query).get('user')
        id = users.get('id')
        print_(f"[SxG]======= Account {index+1}/{sum} [ {users.get('username')} ] ========[SxG]")
        auth = paw.auth(query)
        if auth is not None:
            data = auth.get('data')
            token = data[0]
            datas = data[1]
            userData =datas.get('userData')
            wallet = userData.get('solanaWallet',None)
            allocationData = datas.get('allocationData')
            gameData = datas.get('gameData')
            balance = gameData.get('balance')
            total_balance += balance
            total = allocationData.get('total',0)
            print_(f"Total Balance : {balance}")
            if wallet is None:
                print_('SOL Wallet Address not found')
                address = adresses[index]
                if address is None:
                    print_('Address not found')
                else:
                    paw.connect_sol(token, address)
            else:
                print_(f"Wallet address : {wallet}")


def start():
    print("""
               PAWS BOT
        1. claim
        2. connect wallet ton
        3. connct wallet sol
""")
    choice = input("Enter your choice : ")
    if choice == '1':
        main()
    elif choice == '2':
        connect_ton()
    elif choice == '3':
        connect_sol()
    else:
        print("Invalid choice")

if __name__ == "__main__":
     start()