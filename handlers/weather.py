from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

import asyncio
import os
import requests

# Создание роутера для обработки сообщений
router = Router()

# Функция для получения информации о погоде по названию города
def get_weather(city_name):
    weather_url = "http://api.worldweatheronline.com/premium/v1/weather.ashx"
    params = {
        "key": os.getenv("API_WEATHER"),
        "q": city_name,
        "format": "json",
        "lang": "ru"
    }
    try:     
        result = requests.get(weather_url, params=params)
        result.raise_for_status()
        weather = result.json()
        if "data" in weather:
            if 'current_condition' in weather["data"]:
                return weather['data']['current_condition'][0]
    except(requests.RequestException, ValueError):
        return None

# Обработчик команды /start
@router.message(F.text, Command("start"))
async def start(message: Message):
    await message.answer("Введи название города, чтобы узнать погоду!")
    
# Обработчик текстовых сообщений для получения информации о погоде
@router.message(F.text)
async def get_weather_text(message: Message):
    city_name = message.text
    weather_text = get_weather(city_name)
    if weather_text:
        response = (f"Погода в городе {city_name.title()}:\n"
                    f"Температура: {weather_text['temp_C']}°C\n"
                    f"Влажность: {weather_text['humidity']}%\n"
                    f"Скорость ветра: {weather_text['windspeedKmph']} км/ч\n"
                    f"Давление: {weather_text['pressure']} мм.рт.ст.")
    else:
        response = ('Попробуйте ввести другой город')
    await message.answer(response, parse_mode=ParseMode.HTML)
    await asyncio.sleep(1)
    await message.answer('Введи название города, чтобы узнать погоду!')
