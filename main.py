from database import Topic, config
from screenshot import take_screenshot
import requests
import xml.etree.ElementTree as ET
import telebot
from telebot import apihelper
import time
import threading

CHAT_ID = config.get("main", "chat_id")
TOKEN = config.get("main", "token")
B_TEXT = config.get("message", "button-text")
M_TEXT = config.get("message", "message-text")
IU_UPDATE = config.get("main", "interim_update")

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
    tb = telebot.TeleBot(TOKEN)
    worker = Worker(find_news, tb, take_screenshot)
    worker.start()
    @tb.message_handler(content_types=['text'])
    def text_com(message):
        if message.reply_to_message is not None and message.reply_to_message.from_user.is_bot is not True:  # Проверка на ответ пользователю, а не боту
            tb.delete_message(message.chat.id, message.message_id)
            if str(message.text).startswith('!go'):
                search_key = telebot.types.InlineKeyboardMarkup()
                search_key.add(telebot.types.InlineKeyboardButton(text="Подробнее",
                                                                  url=f"http://google.com/search?q={str(message.text).split('!go ')[1]}"))

                tb.send_message(chat_id=message.chat.id,
                                text=f"⁉ Вы можете получить ответ на свой вопрос перейдя по ссылке ниже: ",
                                reply_markup=search_key,
                                reply_to_message_id=message.reply_to_message.message_id)

            elif str(message.text).startswith('!paste'):
                tb.send_message(chat_id=message.chat.id,
                                text=f"📝 Для того чтобы поделиться кодом или текстом ошибки воспользуйтесь сервисами:\n\n"
                                     f" - https://pastebin.com\n"
                                     f" - https://gist.github.com\n"
                                     f" - https://del.dog\n"
                                     f" - https://linkode.org\n"
                                     f" - https://hastebin.com\n",
                                reply_to_message_id=message.reply_to_message.message_id,
                                disable_web_page_preview=True)


    tb.polling(none_stop=True)



