
import urllib
import requests
import datetime
import json


class BotHandler:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_url(self, url):
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content

    def get_json_from_url(self, url):
        content = self.get_url(url)
        js = json.loads(content)
        return js

    #Gets the updates from telegram with long polling
    def get_updates(self, offset= None):
        url = self.api_url + "getUpdates?timeout=100"
        if offset:
            url += "&offset={}".format(offset)
        js = self.get_json_from_url(url)
        return js

    def get_last_update_id(self, updates):
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)

    def echo_all(self, updates):
        for update in updates["result"]:
            try:
                text = update["message"]["text"]
                chat = update["message"]["chat"]["id"]
                self.send_message(text, chat)
            except Exception as e:
                print(e)

    def get_last_chat_id_and_text(self, updates):
        num_updates = len(updates["result"])
        last_update = num_updates - 1
        text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        return text, chat_id

    #Sends a message with correct encodes
    def send_message(self, text, chat_id):
        text = urllib.parse.quote_plus(text)
        url = self.api_url + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        self.get_url(url)


token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

bot = BotHandler(token)
greetings = "Hello my fellow Booty Hunter! Let the hunt begin ;)"
now = datetime.datetime.now()


def main():
    last_update_id = None
    text, chat = (None, None)

    while True:
       updates = bot.get_updates(last_update_id)
       if len(updates["result"]) > 0:
           last_update_id = bot.get_last_update_id(updates) + 1
           text, chat = bot.get_last_chat_id_and_text(bot.get_updates())
           if text == "hello":
               bot.send_message(greetings, chat)
           elif text == "hunt":
               bot.send_message("Where should we start our booty hunt?", chat)
           elif text == "joão":
               bot.send_message("Don't worry João, you're about to get to best booty of your life! :^)", chat)
           else:
               #bot.echo_all(updates)
               pass


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()