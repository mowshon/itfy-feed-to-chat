from database import Topic, config
import requests
import xml.etree.ElementTree as ET
import telebot
from telebot import apihelper
import time

CHATID = config.get("main", "chat_id")
TOKEN = ""


def find_news():
    items = []
    root = ET.fromstring(requests.get("https://itfy.org/forums/python-help/index.rss").content)
    for i in root.findall('.//channel/item'):
        link, title = i.find('link').text, i.find('title').text
        if not Topic.select().where(Topic.title == title, Topic.link == link):
            items.append({"title": title, "link": link})
            Topic.create(title=title, link=link)
    return items


if __name__ == "__main__":
    #apihelper.proxy = {"https": "use_some"}
    tb = telebot.TeleBot(TOKEN)
    while True:
        for i in find_news():
            tb.send_message(CHATID, "<a href='{}'>Новый вопрос в форуме</a>".format(i['link']),
                            parse_mode='html', disable_web_page_preview=False)
        time.sleep(10)
