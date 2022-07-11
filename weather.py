import requests
import datetime
from config import OWM_TOKEN

token = OWM_TOKEN


def get_weather(city):
    try:
        request = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}&units=metric")
        data = request.json()

        text = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" \
               f"Город : {data['name']}\n" \
               f"Температура сейчас : {data['main']['temp']} °C\n" \
               f"Максимальная температура в течении дня : {data['main']['temp_max']}\n" \
               f"Минимальная температура в течении дня : {data['main']['temp_min']}"
        return text

    except Exception:

        return "Не верный ввод! Попробуйте еще раз!"
