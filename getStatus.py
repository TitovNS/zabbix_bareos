#!/usr/bin/env python3

import argparse
import json
import time

import requests

import getClients


def getStatusJob(accessToken, clientsName):
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {accessToken}',
        'Content-Type': 'application/json',
    }

    response = requests.get(f'{getClients.URL}/control/jobs', headers=headers)
    parsedString = json.loads(response.text)
    time.sleep(3)
    jobs = parsedString["jobs"]
    isNotFound = True
    for i in reversed(jobs):
        if i['client'] == clientsName:
            isNotFound = False
            print(i['jobstatus'])
            break
    if isNotFound:
        print("Client not found!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Help.")
    parser.add_argument("--name", required=True, type=str, help="Enter client's name as an argument.")
    args = parser.parse_args()
    name = args.name

    accessToken = getClients.auth()
    getStatusJob(accessToken, name)
