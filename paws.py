import os
import sys
import random
import string
import requests
import time
import json
from datetime import datetime, timedelta
import requests

class Paws:
    def __init__(self):
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Host': 'api.paws.community',
            'Origin': 'https://app.paws.community',
            'Pragma': 'no-cache',
            'Priority': 'u=3, i',
            'Referer': 'https://app.paws.community/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_(self, word):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"[{now}] | {word}")

    def make_request(self, method, url, headers, json=None, data=None):
        retry_count = 0
        while True:
            time.sleep(2)
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, json=json)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=json, data=data)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=json, data=data)
            else:
                raise ValueError("Invalid method.")
            
            if response.status_code >= 500:
                if retry_count >= 4:
                    self.print_(f"Status Code: {response.status_code} | {response.text}")
                    return None
                retry_count += 1
            elif response.status_code >= 400:
                self.print_(f"Status Code: {response.status_code} | {response.text}")
                return None
            elif response.status_code >= 200:
                return response
    
    def auth(self, query):
        url = 'https://api.paws.community/v1/user/auth'
        payload = {'data':query, 'referralCode':'1mFY7Q2p'}
        headers = {
            **self.headers,
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json'
        }
        try:
            response = self.make_request('post', url=url, headers=headers, json=payload)
            if response is not None:
                return response.json()
            
        except Exception as error:
            self.print_(f"Error {error}")
            return None
    
    def bind_wallet(self, token, address):
        url = 'https://api.paws.community/v1/user/wallet'
        headers = {
            **self.headers,
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        try:
            payload = {
                "wallet": address
            }
            response = self.make_request('post', url=url, headers=headers, json=payload)
            if response is not None:
                jsons = response.json()
                success = jsons.get('success',False)
                if success:
                    self.print_('Bind Wallet Success')
            
        except Exception as error:
            self.print_(f"Error {error}")
            return None
    
    def quest_list(self, token):
        url = 'https://api.paws.community/v1/quests/list'
        headers = {
            'Authorization': f'Bearer {token}'
        }

        response = self.make_request('get', url=url, headers=headers)
        if response is not None:
            jsons = response.json()
            list_data = jsons.get('data',[])
            for data in list_data:
                _id = data.get('_id','')
                title = data.get('title','')
                progress = data.get('progress')
                status = progress.get('status')
                claimed = progress.get('claimed')
                if status == 'finished':
                    self.print_(f"Task {title} Done")
                elif status == 'claimable':
                    if claimed:
                        self.quest_claim(token=token, id=_id, name=title)
                else:
                    if title in ['Connect wallet', 'Invite 10 friends', 'Follow channel', 'Boost PAWS channel']:
                        self.print_(f"Task {title} Skip")
                    else:
                        self.quest_completed(token=token, id=_id, name=title)
    
    def quest_christmas(self, token):
        url = 'https://api.paws.community/v1/quests/list?type=christmas'
        headers = {
            'Authorization': f'Bearer {token}'
        }

        response = self.make_request('get', url=url, headers=headers)
        if response is not None:
            jsons = response.json()
            list_data = jsons.get('data',[])
            for data in list_data:
                _id = data.get('_id','')
                title = data.get('title','')
                progress = data.get('progress')
                status = progress.get('status')
                claimed = progress.get('claimed')
                if status == 'finished':
                    self.print_(f"Task {title} Done")
                elif status == 'claimable':
                    if claimed:
                        self.quest_claim(token=token, id=_id, name=title)
                else:
                    if title in ['Connect wallet', 'Invite 10 friends', 'Follow channel', 'Boost PAWS channel']:
                        self.print_(f"Task {title} Skip")
                    else:
                        self.quest_completed(token=token, id=_id, name=title)

    def quest_completed(self, token, id, name):
        url = 'https://api.paws.community/v1/quests/completed'
        payload = {'questId':id}
        headers = {
            **self.headers,
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        response = self.make_request('post', url=url, headers=headers, json=payload)
        
        if response is not None:
            jsons = response.json()
            data = jsons.get('data',False)
            success = jsons.get('success', False)
            self.print_(f"Checked task {name} {data}")
            if success:
                self.quest_claim(token=token, id=id, name=name)
    
    def quest_claim(self, token, id, name):
        url = 'https://api.paws.community/v1/quests/claim'
        payload = {'questId':id}
        headers = {
            **self.headers,
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        try:
            response = self.make_request('post', url=url, headers=headers, json=payload)
            if response is not None:
                jsons = response.json()
                success = jsons.get('success', False)
                data = jsons.get('data',False)
                if success:
                    self.print_(f"Claimed task {name} {data}")
        except Exception as error:
            self.print_(f"Error {error}")
    
    def connect_sol(self, token, sol_address):
        url = 'https://api.paws.community/v1/user/sol-wallet'
        headers = {
            **self.headers,
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        try:
            payload = {
                "wallet": sol_address
            }
            response = self.make_request('post', url=url, headers=headers, json=payload)
            if response is not None:
                jsons = response.json()
                success = jsons.get('success',False)
                if success:
                    self.print_(f'Bind Wallet Success, Address : {sol_address}')
            
        except Exception as error:
            self.print_(f"Error {error}")
            return None
        