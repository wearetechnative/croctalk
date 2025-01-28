import os
import glob
import requests
from telegram import Update
import telegram_voice
import http.client
from telegram_voice import *
import json
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
SITE = os.getenv('SITE')

headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    'Authorization': f"Bearer {TOKEN}"
    }

async def get_files():
    list_of_files = glob.glob('txt/*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    with open(latest_file, 'r') as latest_input:
        content = latest_input.read()
    return content


async def body_content():
    content = await get_files()
    body = [
        {
            "id": "595b40d5-3095-4667-b8e3-73ab407a52a7",
            "type": "paragraph",
            "props": {
                "textColor": "default",
                "backgroundColor": "default",
                "textAlignment": "left"
            },
            "content": [{"type": "text", "text": str(content), "styles": {}}],
            "children": []
        }
    ]
    body_json = json.dumps(body)
    return body_json

async def note():
    body = await body_content()
    payload = {
        "position": 0,
        "title": f"Telegram: {telegram_voice.current_time}",
        "body": body,
        "createdBy": {
            "source": "SYSTEM"
        }
    }
    payload_json = json.dumps(payload)
    conn = http.client.HTTPConnection(SITE)
    conn.request("POST", "/rest/notes", payload_json, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

async def task():
    body = await body_content()
    payload = {
        "position": 0,
        "title": f"Telegram: {telegram_voice.current_time}",
        "body": body,
        "status": "TODO",
        "createdBy": {
            "source": "SYSTEM"
        }
    }
    payload_json = json.dumps(payload)
    conn = http.client.HTTPConnection(SITE)
    conn.request("POST", "/rest/tasks", payload_json, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

async def opportunity():
    payload = {
        "position": 0,
        "name": f"Telegram: {telegram_voice.current_time}",
        "amount": {
            "amountMicros": 0,
            "currencyCode": "test",
        },
        "stage": "NEW",
        "createdBy": {
            "source": "SYSTEM"
        }
    }
    payload_json = json.dumps(payload)
    conn = http.client.HTTPConnection(SITE)
    conn.request("POST", "/rest/opportunities", payload_json, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


# Use this to attach a note to a opportunity
#import http.client
#
#conn = http.client.HTTPConnection("localhost:3000")
#
#conn.request("POST", "/rest/noteTargets", payload, headers)
#
#res = conn.getresponse()
#data = res.read()
#
#print(data.decode("utf-8"))
