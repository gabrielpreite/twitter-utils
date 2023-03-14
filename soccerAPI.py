#ID SERIE A 135

import json
import requests
from datetime import date, timedelta

def soccer(test=False):
    if not test:
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

        today = date.today()
        yesterday = today - timedelta(days=1)
        yesterday = yesterday.strftime("%Y-%m-%d")

        querystring = {"league":"135","season":"2022","from":"2023-01-15","to":yesterday}

        headers = {
            "X-RapidAPI-Key": "",
            "X-RapidAPI-Host": ""
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        return json.dumps(response.json())
    with open("soccer.json", "r") as f:
        return f.read()

def match(querystring, test=False):
    if not test:
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

        headers = {
            "X-RapidAPI-Key": "",
            "X-RapidAPI-Host": ""
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        return json.dumps(response.json())
    with open("soccer2.json", "r") as f:
        return f.read()