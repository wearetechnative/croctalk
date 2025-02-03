import os
import glob
import requests
import http.client
import main
from main import current_time
import json
from dotenv import load_dotenv
from telegram.ext import Application, MessageHandler, filters, CommandHandler, CallbackQueryHandler, Application, ContextTypes, CallbackContext

load_dotenv()
TOKEN = os.getenv('TOKEN')
SITE = os.getenv('SITE')
SAVE_DIR_TXT = os.getenv('SAVE_DIR_TXT')

headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    'Authorization': f"Bearer {TOKEN}"
    }

async def get_files():
    list_of_files = glob.glob(SAVE_DIR_TXT+"/*")
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

async def connection(context: CallbackContext):

    payload_json = json.dumps(context.user_data["payload"])
    conn = http.client.HTTPSConnection(SITE)
    conn.request("POST", "/rest/"+context.user_data["rest"], payload_json, headers)
    res = conn.getresponse()
    data = res.read()
    response_data = data.decode("utf-8")
    response_json = json.loads(response_data)
    print(response_json)

    if context.user_data["rest"] == "notes":
        id_twenty = response_json["data"]["createNote"]["id"]
        return id_twenty
    elif context.user_data["rest"] == "tasks":
        id_twenty = response_json["data"]["createTask"]["id"]
        return id_twenty
    elif context.user_data["rest"] == "opportunities":
        id_twenty = response_json["data"]["createOpportunity"]["id"]
        return id_twenty

async def note(context: CallbackContext):
    body = await body_content()
    payload = {
        "position": 0,
        "title": f"Telegram - {main.current_time}",
        "body": body,
        "createdBy": {
            "source": "API"
        }
    }
    context.user_data["payload"] = payload
    context.user_data["rest"] = "notes"
    note_id = await connection(context)
    return note_id

async def task(context: CallbackContext):
    body = await body_content()
    payload = {
        "position": 0,
        "title": f"Telegram - {main.current_time}",
        "body": body,
        "status": "TODO",
        "createdBy": {
            "source": "API"
        }
    }
    context.user_data["payload"] = payload
    context.user_data["rest"] = "tasks"
    task_id = await connection(context)
    return task_id


async def opportunity(context: CallbackContext):
    payload = {
        "position": 0,
        "name": f"Telegram - {main.current_time}",
        "stage": "NEW",
        "createdBy": {
            "source": "API"
        }
    }
    context.user_data["payload"] = payload
    context.user_data["rest"] = "opportunities"
    opportunity_id = await connection(context)
    return opportunity_id

async def note_target(context: CallbackContext):
    opportunity_id = await opportunity(context)
    note_id = await note(context)    
    payload = {
    "noteId": note_id,
    "opportunityId": opportunity_id,
    }
    context.user_data["payload"] = payload
    context.user_data["rest"] = "noteTargets"
    await connection(context)

async def task_target(context: CallbackContext):
    opportunity_id = await opportunity(context)
    task_id = await task(context)    
    payload = {
    "taskId": task_id,
    "opportunityId": opportunity_id,
    }
    context.user_data["payload"] = payload
    context.user_data["rest"] = "taskTargets"
    await connection(context)
