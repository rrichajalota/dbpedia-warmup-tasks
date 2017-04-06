import json
import requests
import time
import urllib
import io
import random
from dbHelper import DBHelper
from secrets import bot_token, appid

db = DBHelper() 
URL = "https://api.telegram.org/bot{}/".format(bot_token)
WOLF_URL = "http://api.wolframalpha.com/v2/"
SHORT_ANS_URL = WOLF_URL + "result?appid={}".format(appid)
SIMPLE_ANS_URL = WOLF_URL + "simple?appid={}".format(appid)

def get_url(url):
    """
    sends a GET request to the telegram API
    """
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json(url):
    """
    converts the response from the telegram API into json format
    """
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    """
    receives recent updates from the telegram bot
    """
    url = URL + "getUpdates?timeout=120"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json(url)
    return js

def update_qID(q_id):
    curr_id = int(q_id)
    next_id = curr_id + 1
    return str(next_id)

def inline_queries(updates):
    try:
        for update in updates["result"]:

            print update
            #print update["message"]
            #print update["inline_query"]
            if "message" in update:
                #print "message in keys"
                query_wolframalpha(updates)

            elif "inline_query" in update:
                #print "I am inline!"
                inline_query = update["inline_query"]
                #queryId = update_qID(inline_query["id"])
                queryId = inline_query["id"].decode('utf8')
                print queryId
                querytext = inline_query["query"]
                print querytext

                if inline_query["query"] and querytext != "":

                    print "text is here"
                    url = SHORT_ANS_URL + "&i={}".format(querytext)
                    print url

                    response_from_api = get_url(url) #query the API
                    print response_from_api

                    message = {"message_text": response_from_api, "parse_mode": "Markdown", "disable_web_page_preview": True}

                    sysrandom = random.SystemRandom()
                    q_id = hex(sysrandom.getrandbits(64))

                    #InlineKeyboardMarkup = InlineKeyboard()

                    InlineQueryResultArticle = {"type": "article", "id": q_id, "title": "response from wolframalpha", "input_message_content":message}#, "reply_markup": InlineKeyboardMarkup}
                    results = []
                    results.append(InlineQueryResultArticle)

                    params = {
                        'inline_query_id': queryId,
                        'results' : json.dumps(results),
                        #'cache_time': 3000,
                        'switch_pm_text': "For elaborative queries, switch to chat space",
                        'switch_pm_parameter': 'start',
                    }

                    print params
                    print "------------------------------"
                    reply_at_url = URL + "answerInlineQuery"     
                    print requests.post(reply_at_url, params= params)

            else:
                pass
    except KeyError:
        pass


def query_wolframalpha(updates):
    """
    sends the search query to the wolframalpha api and receives the response from it
    """
    
    for update in updates["result"]:
        
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]

            if text == "/start":
                send_message("Hi! I'm a simple Question-Answering bot. Ask me anything you want to or type /commands to check which commands I accept!", chat)

            elif text == "/commands":
                send_message("Type: \n /history - to see your search queries \n /bothistory - to see what others searched for", chat)
            
            elif text == "/history":
                searches = db.user_query(chat)
                keyboard = build_keyboard(searches)
                send_message("You can also select from your past queries! \n Feel free to ask again!! :)", chat, keyboard)

            elif text == "/bothistory":
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
                url = SIMPLE_ANS_URL + "&input={}&layout=labelbar&fontsize=24".format(text)
                sendImage(url, chat)

        except KeyError:
            pass

#used when simple_api of wolframalpha is accessed
def sendImage(result_url, chat_id):
    """
    sends Images to the telegram bot which are a part of the descriptive response from the wolframalpha api
    """
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
    """
    returns the last update_id received from the telegram api to set the offset value for the next update
    """
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

#builds a custom keyboard
def build_keyboard(queries):
    """
    returns a custom keyboard
    """
    keyboard = [[query] for query in queries]
    reply_markup = {"keyboard" : keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def send_message(text, chat_id, reply_markup= None, encode=True):
    """
    sends a message from the telegram bot to the user
    """
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
            #query_wolframalpha(updates)
            inline_queries(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()