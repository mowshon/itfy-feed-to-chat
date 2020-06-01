import os
from database import Topic, config
import apiai
import json
from screenshot import take_screenshot
import requests
import xml.etree.ElementTree as ET
import telebot
from telebot import apihelper
import time
import threading
from add_data_in_tp import add_tp

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.get("dialogflow", "key")
DIALOGFLOW_ID = config.get("dialogflow", "id")
DF_PROJECT_ID = config.get("dialogflow", "project_id")
DF_HELP_UUID = config.get("dialogflow", "help_intent_uuid")
DF_PASS_UUID = config.get("dialogflow", "pass_intent_uuid")
CHAT_ID = config.get("main", "chat_id")
TOKEN = config.get("main", "token")
B_TEXT = config.get("message", "button-text")
M_TEXT = config.get("message", "message-text")
IU_UPDATE = config.get("main", "interim_update")
QUESTION_TEXT = config.get("message", "question-body")
DETAIL_TEXT = config.get("message", "detailed-text")
PASTE_TEXT = config.get("message", "paste-text")
NOMETA_TEXT = config.get("message", "nometa-body")
NEPRIVET_TEXT = config.get("message", "neprivet-text")
IMPORT_DATA_FAIL = config.get("message", "import-data-fail")
ADMINS = config.get("main", "admins").split(",")


def find_news():
    items = []
    try:
        root = ET.fromstring(requests.get(config.get('main', 'rss_url')).content)
    except requests.exceptions.ConnectionError:
        return []
    for item in root.findall('.//channel/item'):
        link, title = item.find('link').text, item.find('title').text
        ext_id = link.split('.')[-1].split('/')[0]
        if not Topic.select().where(Topic.ext_id == ext_id):
            items.append({"title": title, "link": link})
            Topic.create(title=title, link=link, ext_id=ext_id)
        else:
            Topic.update(title=title, link=link).where(Topic.ext_id == ext_id)
    return items


class Worker(threading.Thread):
    def __init__(self, find_news, bot, take_screenshot_func):
        super(Worker, self).__init__()
        self.find_news = find_news
        self.bot = bot
        self.take_screenshot = take_screenshot_func

    def run(self):
        while True:
            for i in self.find_news():
                key = telebot.types.InlineKeyboardMarkup()
                key.add(telebot.types.InlineKeyboardButton(text=f"{B_TEXT}", url=i['link']))
                if self.take_screenshot(i['link']):
                    photo = open('attachement.png', 'rb')
                    self.bot.send_photo(chat_id=CHAT_ID, photo=photo,
                                        caption=f"{M_TEXT} <a href='{i['link']}'>{i['title']}</a>",
                                        parse_mode='html',
                                        reply_markup=key
                                        )
                else:
                    self.bot.send_message(chat_id=CHAT_ID,
                                          text=f"<a href='{i['link']}'>{M_TEXT}</a>",
                                          disable_web_page_preview=False,
                                          parse_mode='html',
                                          reply_markup=key)
            time.sleep(int(IU_UPDATE))


if __name__ == "__main__":
    # apihelper.proxy = {"https": "use_some"}
    bot = telebot.TeleBot(TOKEN)
    worker = Worker(find_news, bot, take_screenshot)
    worker.start()

    commands = ('!go', '!paste', '!np', '!nm', '!dnm')  # Bot`s commands. If you add a new command add it here!

    @bot.message_handler(content_types=['text'])
    def text_com(message):
        username = message.from_user.username
        request = apiai.ApiAI(f'{DIALOGFLOW_ID}').text_request()
        request.lang = 'ru'
        request.session_id = 'xyu'
        request.query = message.text
        responseJson = json.loads(request.getresponse().read().decode('utf-8'))
        response = responseJson['result']['fulfillment']['speech']
        try:
            photo = message.photo.file_size
        except AttributeError:
            photo = 0
        if response and photo == 0:
            tailkey = telebot.types.InlineKeyboardMarkup()
            tailkey.add(telebot.types.InlineKeyboardButton(text=DETAIL_TEXT,
                                                              url=f"https://neprivet.ru"))
            tailkey.add(telebot.types.InlineKeyboardButton(text=DETAIL_TEXT,
                                                           url=f"https://nometa.xyz"))
            bot.send_message(chat_id=message.chat.id, text=response, reply_to_message_id=message.message_id, reply_markup=tailkey)
        if message.reply_to_message is not None and message.reply_to_message.from_user.is_bot is not True:  # Check if replied message is replied to a human
            try:
                if str(message.text).startswith(commands):  # Check if user has used any of those commands
                    bot.delete_message(message.chat.id, message.message_id)
            except Exception as DelError:
                print(f"DelError: {DelError}")
            if str(message.text).startswith('!go'):  # Google
                try:  # Checking that query is not empty
                    search_query = str(message.text).split('!go ')[1]
                except IndexError:
                    search_query = 'Как правильно задавать вопросы на сообществе'

                search_key = telebot.types.InlineKeyboardMarkup()
                search_key.add(telebot.types.InlineKeyboardButton(text=DETAIL_TEXT,
                                                                  url=f"http://google.com/search?q={search_query}"))

                bot.send_message(chat_id=message.chat.id,
                                 text=QUESTION_TEXT,
                                 reply_markup=search_key,
                                 reply_to_message_id=message.reply_to_message.message_id)

            elif str(message.text).startswith('!paste'):  # Pastebin
                bot.send_message(chat_id=message.chat.id,
                                 text=PASTE_TEXT,
                                 reply_to_message_id=message.reply_to_message.message_id,
                                 disable_web_page_preview=True)

            elif str(message.text).startswith('!nm'):  # nometa.xyz
                if username in ADMINS:  # Bot checks if user is in admins so randoms can't use this a lot
                    data2input = message.reply_to_message.text
                    try:
                        add_tp(DF_HELP_UUID, DF_PROJECT_ID, message=f'{data2input}')
                    except Exception:
                        bot.send_message(
                            chat_id=message.chat.id,
                            reply_markup=None,
                            text=IMPORT_DATA_FAIL
                        )
                    nometa_key = telebot.types.InlineKeyboardMarkup()
                    nometa_key.add(telebot.types.InlineKeyboardButton(text=DETAIL_TEXT, url="http://nometa.xyz"))
                    bot.send_message(chat_id=message.chat.id,
                                    text=NOMETA_TEXT,
                                    reply_markup=nometa_key,
                                    reply_to_message_id=message.reply_to_message.message_id)
                else:
                    bot.send_message(chat_id=message.chat.id,
                                    text=f'@{username}, пожалуйста, если Вы считаете, что это мета-вопрос или просто "Привет", оповестите об этом администрацию. Спасибо!',
                                    )

            elif str(message.text).startswith('!np'):  # neprivet.ru
                if username in ADMINS:  # Bot checks if user is in admins so randoms can't use this a lot
                    data2input = message.reply_to_message.text
                    try:
                        add_tp(DF_HELP_UUID, DF_PROJECT_ID, message=f'{data2input}')
                    except Exception:
                        bot.send_message(
                            chat_id=message.chat.id,
                            reply_markup=None,
                            text=IMPORT_DATA_FAIL
                        )
                    nometa_key = telebot.types.InlineKeyboardMarkup()
                    nometa_key.add(telebot.types.InlineKeyboardButton(text=DETAIL_TEXT, url="http://neprivet.ru"))
                    bot.send_message(chat_id=message.chat.id,
                                    text=NEPRIVET_TEXT,
                                    reply_markup=nometa_key,
                                    reply_to_message_id=message.reply_to_message.message_id)
                else:
                    bot.send_message(chat_id=message.chat.id,
                                    text=f'@{username}, пожалуйста, если Вы считаете, что это мета-вопрос или просто "Привет", оповестите об этом администрацию. Спасибо!',
                                    )
            elif str(message.text).startswith('!dnm'):  # if that's not a meta-question
                if username in ADMINS:  # Bot checks if user is in admins so randoms can't use this a lot
                    data2input = message.reply_to_message.text
                    try:
                        add_tp(DF_PASS_UUID, DF_PROJECT_ID, message=f'{data2input}')
                    except Exception:
                        bot.send_message(
                            chat_id=message.chat.id,
                            reply_markup=None,
                            text=IMPORT_DATA_FAIL
                        )
                    bot.send_message(chat_id=message.chat.id,
                                    text='Ошибся, извините =)',
                                    reply_to_message_id=message.reply_to_message.message_id)
                else:
                    bot.send_message(chat_id=message.chat.id,
                                    text=f'@{username}, пожалуйста, если Вы считаете, что это не мета-вопрос и не просто "Привет", оповестите об этом администрацию. Спасибо!',
                                    )

    bot.polling(none_stop=True)