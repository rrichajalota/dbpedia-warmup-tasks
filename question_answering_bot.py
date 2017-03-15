import json
import requests
import time
import urllib
import io
from dbHelper import DBHelper
from secrets import bot_token, APP_NAME, appid

db = DBHelper() 
URL = "https://api.telegram.org/bot{}/".format(bot_token)
WOLF_URL = "http://api.wolframalpha.com/v2/"
SHORT_ANS_URL = WOLF_URL + "result?appid={}".format(appid)
SIMPLE_ANS_URL = WOLF_URL + "simple?appid={}".format(appid)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def query_wolframalpha(updates):
    
    for update in updates["result"]:
        
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]

            if text == "/start":
                send_message("Hi! I'm a simple Question-Answering bot. Send /commands to check which commands I accept!", chat)

            elif text == "/commands":
                send_message("/history - to see your search queries", chat)
            
            elif text == "/history":
                searches = db.user_query(chat)
                keyboard = build_keyboard(searches)
                send_message("You can also select from your past queries!Feel free to ask again!! :)", chat, keyboard)

            elif text == "/bot_history":
                searches = db.all_query()
                keyboard = build_keyboard(searches)
                send_message("These are the queries asked by others!", chat, keyboard)
            
            elif text.startswith("/"):
                continue
            
            else: #send the query to wolframalpha 
                db.add_query(text,chat)
                send_message("Looking for a short answer..", chat)
                url = SHORT_ANS_URL + "&i={}".format(text)
                send_message(get_url(url), chat) 
                send_message("Let me search for a descriptive one..", chat)
                url = SIMPLE_ANS_URL + "&input={}&layout=labelbar&fontsize=22".format(text)
                sendImage(url, chat)

        except KeyError:
            pass

#used when simple_api of wolframalpha is accessed
def sendImage(result_url, chat_id):
    response = requests.get(result_url)
    photo = io.BytesIO(response.content)
    photo.name = 'img.png'
    data = {'chat_id': chat_id}
    files = {'photo': photo}
    telegram_url = URL + "sendPhoto"
    r = requests.post(telegram_url, files = files, data = data)
    print(r.status_code, r.reason, r.content)
    if (r.status_code != 200):
        send_message("Oops. I don't know! :(", chat_id)


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

#builds a custom keyboard
def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard" : keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def send_message(text, chat_id, reply_markup= None, encode=True):
    try:
        if encode == True:
            text = urllib.quote(text.encode('UTF-8'))
        url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
        if reply_markup:
            url += "&reply_markup={}".format(reply_markup)
        get_url(url)
    except AttributeError:
        text = "No result found"
        url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
        get_url(url)


def main():
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            query_wolframalpha(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()