from bs4 import BeautifulSoup
import requests
from googletrans import Translator


# Вспомогательная функция для перевода города с русского на английский для scrapping_weather
def translate_city(city):
    translator = Translator()
    result = translator.translate(city, dest='en').text.lower()
    return result


# Функция узнающаю температуру в городе
def scrapping_weather(city):
    try:
        url = f"https://www.ventusky.com/ru/{translate_city(city)}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        temp_info = soup.find('td', class_='temperature').text.replace('\n', '').strip().split()[0]
        return temp_info
    except Exception:
        return False
