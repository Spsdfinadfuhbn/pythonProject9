import asyncio
from aiogram.types import FSInputFile
from datetime import date, timedelta
import matplotlib.pyplot as plt
import dp
import numpy as numpy
from aiogram.client import bot
from telebot import types
from aiogram import *
from aiogram.filters.command import Command
import logging
import os
import requests


TOKEN = "6613970622:AAHdXz77HCjmA6ybSHCcgAl_JXLWLedrXYA"
bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    kb = [
        [types.KeyboardButton(text="цена акции apple")],
        [types.KeyboardButton(text="цена акции google")],
        [types.KeyboardButton(text="цена акции amazon")],
        [types.KeyboardButton(text="поставить оценку")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("Что надо?", reply_markup=keyboard)
    with open("id.txt","a") as f:
        f.write(f"{user_id}\n")



@dp.message(F.text.lower() == "цена акции apple")
async def send_price(message: types.Message):
    today = date.today() - timedelta(days=1)
    if not os.path.exists(f"AAPL{today}.png"):
        create_graphicks('AAPL')
    photo = FSInputFile(path="AAPL.png")
    await bot.send_photo(chat_id=message.chat.id,photo=photo)
    await message.reply(str(get_data("AAPL")))



@dp.message(F.text.lower() == "цена акции amazon")
async def send_price_amazon(message: types.Message):
    create_graphicks('AMZN')
    photo = FSInputFile(path="AMZN.png")
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    await message.reply(str(get_data("AMZN")))



@dp.message(F.text.lower() == "цена акции google")
async def send_price_google(message: types.Message):
    create_graphicks('GOOG')
    photo = FSInputFile(path="GOOG.png")
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
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
        [types.KeyboardButton(text="посмотреть отзывы бота")],
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


@dp.message(F.text.lower() == 'посмотреть отзывы бота')
async def send_assessments(message: types.Message):
    await message.answer('вот отзывы, которые написали пользователи :')
    with open("marks.txt", "r") as f:
        counter = f.read()
        await message.answer(counter)


@dp.message(F.text.lower() == 'назад')
async def send_asse(message: types.Message):
    await cmd_start(message)



@dp.message(F.text.lower() == 'оставить отзыв в виде сообшения')
async def send_write_message(message: types.Message):
    today = date.today() - timedelta(days=1)
    await steal(message)

    @dp.message()  # реагирует на любые сообщения
    def test(message):
        with open("marks.txt", "a", encoding="utf-8") as f:
            print(type(message.text))
            f.write("{} {}\n".format(today, message.text))



apiKey = "Kw01MECyf6902xX3s5plA1cPEwS0pQIe"


def get_data(ticker):
    today = date.today() - timedelta(days=1)
    print(today)
    res = requests.get(
        f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{today}/{today}?adjusted=true&sort=asc&limit=120&apiKey={apiKey}")
    data = res.json()
    data_json = data['results'][0]['h']
    with open('response.json', 'w') as f:
        f.write(str(data))
    return data_json


def get_data2_0(ticker):
    today = date.today() - timedelta(days=1)
    week_ago = date.today() - timedelta(days=7)
    dates = []
    for i in range(1, 9):
        dates.append(str(date.today() - timedelta(days=i)))
    print(today)
    res = requests.get(
        f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{week_ago}/{today}?adjusted=true&sort=asc&limit=120&apiKey={apiKey}")
    data = res.json()
    data_json = []
    for i in range(0, len(data['results'])):
        data_json.append(data['results'][i]['h'])
    with open('response.json', 'w') as f:
        f.write(str(data))
    return data_json

def create_graphicks(ticker):
    today = date.today() - timedelta(days=1)
    yesterday = date.today() - timedelta(days=2)
    week_ago = date.today() - timedelta(days=7)
    if os.path.exists(f"{ticker}{yesterday}.png"):
        os.remove(f"{ticker}{yesterday}.png")
    data_json = get_data2_0(ticker)
    plot_data = numpy.array(data_json)
    plt.plot(numpy.arange(0,5,1), plot_data)
    plt.xlabel(f"{today};{week_ago}")
    plt.savefig(f"{ticker}{today}.png")
    plt.clf()
    return plot_data


@dp.message()
async def steal(message: types.Message):
    s=open('messages.txt', 'a', encoding="utf-8")
    s.write(f"{message.from_user.username}   -   message is   {message.text}\n")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
 asyncio.run(main())