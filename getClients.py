#!/usr/bin/env python3

import json

import requests
import configparser

config = configparser.ConfigParser()
config.read("./settings.ini")       #путь до файла с данными пользователся webui bareos 
USERNAME = config["Director"]["username"]
PASSWORD = config["Director"]["password"]
URL = config["Director"]["url"]


def auth():
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'grant_type': '',
        'username': USERNAME,
        'password': PASSWORD,
        'scope': '',
        'client_id': '',
        'client_secret': ''
    }

    response = requests.post(f'{URL}/token', headers=headers, data=data)
    parsedString = json.loads(response.text)
    accessToken = parsedString["access_token"]
    return accessToken


def get_client(accessToken):
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {accessToken}',
    }

    params = (
        ('verbose', 'yes'),
    )

    response = requests.get(f'{URL}/configuration/clients?verbose=yes', headers=headers)
    parsedString = json.loads(response.text)

    clients = parsedString["clients"]
    listClient = clients.keys()
    clientsArr = []
    for i in listClient:
        if clients[i]['enabled'] == True and i != 'bareos-fd':
            d = {"{#CLIENT}": i}
            clientsArr.append(d)
    json_string = json.dumps(clientsArr)
    print(json_string)


if __name__ == '__main__':
    accessToken = auth()
    get_client(accessToken)
