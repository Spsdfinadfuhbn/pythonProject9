import asyncio
import time
import config
from datetime import date, timedelta
from unittest.mock import call

import dp
import telebot
from aiogram.client import *
from aiogram.client import bot
from telebot import types
from aiogram import *
from aiogram.filters.command import Command
from telebot.asyncio_helper import get_chat
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters, InlineQueryHandler
import logging
import requests
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@dp.message(content_types=['text'])  #реагирует на любые сообщения
def test(message):
     if message.text == 'One':    #Если содержимое == 'One',то
          bot.reply_to(message, 'Введите текст')   #Bot reply 'Введите текст'
          @bot.message_handler(content_types=['text'])  #Создаём новую функцию ,реагирующую на любое сообщение
          def message_input_step(message):
               global text  #объявляем глобальную переменную
               text = message.text
               bot.reply_to(message, f'Ваш текст: {message.text}')
          bot.register_next_step_handler(message, message_input_step) #добавляем следующий шаг, перенаправляющий пользователя на message_input_step


TOKEN = "6613970622:AAHdXz77HCjmA6ybSHCcgAl_JXLWLedrXYA"
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
dp = Dispatcher()
bot = Bot(token="6613970622:AAHdXz77HCjmA6ybSHCcgAl_JXLWLedrXYA")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="цена акции apple")],
        [types.KeyboardButton(text="цена акции google")],
        [types.KeyboardButton(text="цена акции amazon")],
        [types.KeyboardButton(text="поставить оценку")]

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


@dp.message(F.text.lower() == "поставить оценку")
async def cmd_feedback(message: types.Message):
    kb = [
        [types.KeyboardButton(text="1")],
        [types.KeyboardButton(text="2")],
        [types.KeyboardButton(text="3")],
        [types.KeyboardButton(text="4")],
        [types.KeyboardButton(text="5")],
        [types.KeyboardButton(text="посмотреть оценки бота")],
        [types.KeyboardButton(text="оставить отзыв в виде сообшения")],
        [types.KeyboardButton(text="назад")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("поставьте оценку боту", reply_markup=keyboard)


@dp.message(F.text.lower() == "1")
async def send_message(message: types.Message):
    today = date.today() - timedelta(days=1)
    mark = "1"
    await message.answer("Нам очень жаль, что вам не понравилось:( .Напишите пожалуйста, что вам не понравилось,"
                         " мы постараемся это исправить ")
    with open("reviews.txt", "a") as f:
        f.write(f"{today} {mark}\n")


@dp.message(F.text.lower() == "2")
async def send(message: types.Message):
    today = date.today() - timedelta(days=1)
    mark = "2"
    await message.answer("Нам очень жаль, что вам не понравилось:( . Напишите пожалуйста, что вам не понравилось,"
                         " мы постараемся это исправить ")
    with open("reviews.txt", "a") as f:
        f.write(f"{today} {mark}\n")


@dp.message(F.text.lower() == "3")
async def send3(message: types.Message):
    today = date.today() - timedelta(days=1)
    mark = "3"
    await message.answer("Нам очень жаль, что вам не понравилось:( . Напишите пожалуйста, что вам не понравилось, "
                         "а что понравилось, то, что не понравилось, мы постараемся  исправить ")
    with open("reviews.txt", "a") as f:
        f.write(f"{today} {mark}\n")


@dp.message(F.text.lower() == "4")
async def send4(message: types.Message):
    today = date.today() - timedelta(days=1)
    mark = "4"
    await message.answer("Мы рады, что вам  понравилось :) . Напишите пожалуйста, что вам  понравилось, "
                         "а что не понравилось. То, что  не понравилось, мы постараемся  исправить ")
    with open("reviews.txt", "a") as f:
        f.write(f"{today} {mark}\n")


@dp.message(F.text.lower() == "5")
async def send5(message: types.Message):
    today = date.today() - timedelta(days=1)
    mark = "5"
    await message.answer("Мы рады, что вам всё понравилось :) . Напишите пожалуйста, что вам понравилось ")
    with open("reviews.txt", "a") as f:
        f.write(f"{today} {mark}\n")


@dp.message(F.text.lower() == 'посмотреть оценки бота')
async def send_assessments(message: types.Message):
    await message.answer('вот оценки, которые пользователи поставили боту:')
    with open("reviews.txt", "r") as f:
        counter = f.read()
        await message.answer(counter)


@dp.message(F.text.lower() == 'назад')
async def send_asse(message: types.Message):
    await cmd_start(message)


@dp.message(F.text.lower() == 'оставить отзыв в виде сообшения')
async def send_write_message(message: types.Message):
    today = date.today() - timedelta(days=1)
    with open("reviews.txt", "a") as f:
        f.write(f"{today}\n")


apiKey = "Kw01MECyf6902xX3s5plA1cPEwS0pQIe"


def get_data(ticker):
    today = date.today() - timedelta(days=1)
    res = requests.get(
        f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{today}/{today}?adjusted=true&sort=asc&limit=120&apiKey={apiKey}")
    data = res.json()
    data_json = data['results'][0]['h']
    with open('response.json', 'w') as f:
        f.write(str(data))
    print(res)
    return data_json


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
