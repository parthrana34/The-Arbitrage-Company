# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 22:02:33 2019

@author: USER
"""

import pandas as pd 
import json
import requests
from socketIO_client import SocketIO

TRADING_API_URL = 'https://api-demo.fxcm.com:443'
WEBSOCKET_PORT = 443

ACCESS_TOKEN = '43984b3e1a1e13563503cc8af5945831ef337a45'

def on_connect():
    print('websocket Connected: ' + socketIO._engineIO_session.id)

def on_close():
    print('Websocket Closed.')

socketIO = SocketIO(TRADING_API_URL, WEBSOCKET_PORT, params={'access_token': ACCESS_TOKEN})

socketIO.on('connect',on_connect)
socketIO.on('disconnect',on_close)

bearer_access_token = "Bearer " + socketIO._engineIO_session.id + ACCESS_TOKEN

print(bearer_access_token)

method = '/subscribe'

sub_response = requests.post(TRADING_API_URL + method,
                             headers = {
                                     'User-Agent': 'request',
                                     'Authorization': bearer_access_token,
                                     'Accept': 'application/json',
                                     'Content-Type': 'application/x-www-form-urlencoded'
                                     },
                                     data = {
                                             'pairs': 'EUR/USD'
                                             })

print(sub_response)
print(sub_response.json())


def on_price_update(msg):
    response = json.loads(msg)
    print(response)

if sub_response.status_code == 200:
    socketIO.on('EUR/USD', on_price_update)
    #socketIO.on('USD/EUR', on_price_update)
    socketIO.wait()
