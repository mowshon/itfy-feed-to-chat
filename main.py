from database import Topic, config
from screenshot import take_screenshot
import requests
import xml.etree.ElementTree as ET
import telebot
from telebot import apihelper
import time

CHAT_ID = config.get("main", "chat_id")
TOKEN = config.get("main", "token")
B_TEXT = config.get("message", "button-text")
M_TEXT = config.get("message", "message-text")


def find_news():
    items = []
    root = ET.fromstring(requests.get(config.get('main', 'rssurl')).content)
    for item in root.findall('.//channel/item'):
        link, title = item.find('link').text, item.find('title').text
        ext_id = link.split('.')[-1].split('/')[0]
        if not Topic.select().where(Topic.ext_id == ext_id):
            items.append({"title": title, "link": link})
            Topic.create(title=title, link=link, ext_id=ext_id)
        else:
            Topic.update(title=title, link=link).where(Topic.ext_id == ext_id)
    return items


if __name__ == "__main__":
    # apihelper.proxy = {"https": "use_some"}
    tb = telebot.TeleBot(TOKEN)
    while True:
        for i in find_news():
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton(text=f"{B_TEXT}", url=i['link']))
            if take_screenshot(i['link']):
                photo = open('attachement.png', 'rb')
                tb.send_photo(chat_id=CHAT_ID, photo=photo,
                              caption=f"{M_TEXT} <a href='{i['link']}'>{i['title']}</a>",
                              parse_mode='html',
                              reply_markup=key
                              )
            else:
                tb.send_message(chat_id=CHAT_ID,
                            text=f"<a href='{i['link']}'>{M_TEXT}</a>",
                            disable_web_page_preview=False,
                            parse_mode='html',
                            reply_markup=key)
        time.sleep(60)
