import requests
import xml.etree.ElementTree as ET
import sqlite3
import telebot
from telebot import apihelper
import time
DBNAME = "rssfeeder.db"
CHATID = -1001399056118 #@python_scripts
TOKEN = ""


class Feeder:
    def __init__(self):
        self.check_db()
        self.connection = None
        self.cursor = None

    def check_db(self):
        self.connection = sqlite3.connect("rssfeeder.db")
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute("SELECT * FROM feedcache")
        except sqlite3.OperationalError:
            self.cursor.execute("CREATE table feedcache(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, link TEXT)")
            self.connection.commit()

    def find_news(self):
        items = []
        root = ET.fromstring(requests.get("https://itfy.org/forums/python-help/index.rss").content)
        for i in root.findall('.//channel/item'):
            link, title = i.find('link').text, i.find('title').text
            self.cursor.execute("SELECT 1 FROM feedcache WHERE link=?",(link,))
            if not self.cursor.fetchone():
                items.append({"title": title, "link": link})
                self.cursor.execute("INSERT INTO feedcache(link) VALUES(?)",(link,))
        self.connection.commit()
        return items


if __name__ == "__main__":
    #apihelper.proxy = {"https": "some_proxy_if_needed"}
    tb = telebot.TeleBot(TOKEN)
    feed = Feeder()
    while True:
        for i in feed.find_news():
            tb.send_message(CHATID, "Новый вопрос в форуме: <a href='{}'>{}</a>".format(i['link'], i['title']),
                            parse_mode='html', disable_web_page_preview=True)
            time.sleep(10)
