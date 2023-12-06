from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters, InlineQueryHandler
import logging
import datetime
import requests
import telebot
from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
TOKEN = "6613970622:AAHdXz77HCjmA6ybSHCcgAl_JXLWLedrXYA"
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="HI, can i help you?")


def menu():
    urlkb = InlineKeyboardMarkup(row_width=1)
    urlButton = InlineKeyboardButton(text="", url="")
    urlButton2 = InlineKeyboardButton(text="", url="")
    urlkb.add(urlButton, urlButton2)

def answer(update, context):
    text = 'answer:' + update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id,text=text)


def caps(update, context):
    if context.args:
        text_caps = ' '.join(context.args).upper()
        context.bot.send_message(chat_id=update.effective_chat.id,text=text_caps)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,text='No command argument')
        context.bot.send_message(chat_id=update.effective_chat.id,text='send: /caps argument')


def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Convert to UPPER TEXT',
            input_message_content=InputTextMessageContent(query.upper())))
    context.bot.answer_inline_query(update.inline_query.id, results)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command.")

def get_data():
        req = requests.get("https://yobit.net/api/3/ticker/btc_usd")
        response = req.json()
        print(response)
        sell_price = response["btc_usd"]["sell"]
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nSell BTC price: {sell_price}")
        volume = response["btc_usd"]["vol"]
        print(f"\namount BTC: {volume}")

def time_def(TOKEN):
    #% d: день месяца в виде числа % m: порядковый номер месяца % y: год в виде 2 - х чисел % Y: год в виде 4 - х  чисел
   # % H: час в 24 - х часовом формате % M: минута % S: секунда
    from datetime import datetime
    deadline = datetime.strptime("22/11/2023", "%d/%m/%Y")
    print(deadline)

    deadline = datetime.strptime("22/11/2023 12:30", "%d/%m/%Y %H:%M")
    print(deadline)

    deadline = datetime.strptime("11-22-2023 12:30", "%m-%d-%Y %H:%M")
    print(deadline)

    bot = telebot.TeleBot(TOKEN)

    @bot.message_handler(commands=["price"])
    def send_text(message):
         if message.text.lower() == "/price":
            try:
                req = requests.get("https://yobit.net/api/3/ticker/btc_usdt")
                response = req.json()
                sell_price = response["btc_usdt"]["sell"]
                volume = response["btc_usdt"]["vol"]
                bot.send_message(
                    message.chat.id,
                    f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nSell BTC price: {sell_price}"
                    f"\nVolume: {volume}")
            except Exception as ex:
                    print(ex)
                    bot.send_message(message.chat.id, "Something was wrong...")
                    bot.polling()


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


echo_handler = MessageHandler(Filters.text & (~Filters.command), answer)
dispatcher.add_handler(echo_handler)


caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)


inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)


unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)


updater.start_polling()

updater.idle()