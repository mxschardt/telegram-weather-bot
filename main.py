from dataclasses import dataclass
import os
import telebot
import requests
import locale
from datetime import datetime

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))


@dataclass
class WeatherForecast:
    city: str
    date: datetime
    max_temperature: float
    min_temperature: float
    temperature_unit: str
    precipitation: float
    precipitation_unit: str
    uv_index: float
    wind_speed: float
    wind_speed_unit: str


@bot.message_handler(commands=['start'])
def send_welcome(message):
    response = "Привет! Я крайне простой бот для прогноза погоды.\nСоздан Максимом Шардтом из 2об_ИВТ-1/21"
    bot.send_message(message.chat.id,
                     response)


@bot.message_handler(commands=['today'])
def send_forecast_today(message):

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast?latitude=59.94&longitude=30.31&daily=temperature_2m_max,temperature_2m_min,uv_index_max,precipitation_sum,windspeed_10m_max,windgusts_10m_max&forecast_days=1&timezone=Europe%2FMoscow"
    )
    if response.status_code == 200:
        data = response.json()
        weather = WeatherForecast(
            city='Санкт-Петербург',
            date=datetime.strptime(
                data.get('daily').get('time')[0], '%Y-%m-%d').strftime('%d %B, %Y'),
            max_temperature=data.get('daily').get('temperature_2m_max')[0],
            min_temperature=data.get('daily').get('temperature_2m_min')[0],
            precipitation=data.get('daily').get('precipitation_sum')[0],
            uv_index=data.get('daily').get('uv_index_max')[0],
            wind_speed=data.get('daily').get('windspeed_10m_max')[0],
            temperature_unit=data.get('daily_units').get('temperature_2m_max'),
            precipitation_unit=data.get(
                'daily_units').get('precipitation_sum'),
            wind_speed_unit=data.get('daily_units').get('windspeed_10m_max')
        )

    else:
        print('Error: Не удалось получить данные от API.')

    bot_response = f'''{weather.city}
{weather.date}

*{weather.max_temperature}* {weather.temperature_unit} / *{weather.min_temperature}* {weather.temperature_unit}

• Осадки: {weather.precipitation} {weather.precipitation_unit}
• UV index: {weather.uv_index}
• Скорость Ветра: {weather.wind_speed} {weather.wind_speed_unit}'''

    print(bot_response)
    bot.send_message(message.chat.id,
                     bot_response,
                     parse_mode='markdown')


if __name__ == '__main__':
    bot.infinity_polling()
