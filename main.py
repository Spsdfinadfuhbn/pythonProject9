import asyncio
from datetime import date, timedelta

from aiogram import *
from aiogram.filters.command import Command
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters, InlineQueryHandler
import logging
import requests
import telebot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = ""
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
dp = Dispatcher()
bot = Bot(token="")




logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


#def start(update, context):
    #context.bot.send_message(chat_id=update.effective_chat.id, text=get_data())



@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="цена акции apple")],
        [types.KeyboardButton(text="цена акции google")],
        [types.KeyboardButton(text="цена акции amazon")],
        [types.KeyboardButton(text="поставьте оценку")]

    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("Что надо?", reply_markup=keyboard)

@dp.message(F.text.lower() == "цена акции apple")
async def send_price(message: types.Message):
    await message.reply(str(get_data("AAPL")))


@dp.message(F.text.lower() == "цена акции amazon")
async def send_price_amazon(message: types.Message):
    await message.reply(str(get_data("AMZN")))

@dp.message(F.text.lower() == "цена акции google")
async def send_price_google(message: types.Message):
    await message.reply(str(get_data("GOOG")))


@dp.message(F.text.lower() == "поставьте оценку")
async def cmd_feedback(message: types.Message):
    kb = [
        [types.KeyboardButton(text="1")],
        [types.KeyboardButton(text="2")],
        [types.KeyboardButton(text="3")],
        [types.KeyboardButton(text="4")],
        [types.KeyboardButton(text="5")],
        [types.KeyboardButton(text="назад")]

    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("поставьте оценку боту", reply_markup=keyboard)
@dp.message(F.text.lower() == "1")
async def send(message: types.Message):
    await message.answer("Нам очень жаль, что вам не понравилось:( ")
    with open("reviews.txt", "a") as f:
        f.write("1")




apiKey = ""


def get_data(ticker):
    today = date.today()-timedelta(days=1)
    res = requests.get(
        f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{today}/{today}?adjusted=true&sort=asc&limit=120&apiKey={apiKey}")
    data = res.json()
    data_json = data['results'][0]['h']
    file = open('response.json', 'a')
    file.write(str(data))
    file.close()
    print(res)
    return data_json



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
