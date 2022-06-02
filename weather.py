#!/usr/bin/python3

"""
Output all the necessary information about the current weather
in the region where your IP address is locate.
"""

import os
import json
from typing import List, Dict

import requests
from lxml import etree


def get_city() -> str:
    """Gets name of your city by IP address from yandex.ru/internet."""

    information: requests.Response = requests.get("https://yandex.ru/internet")

    html: etree.Element = etree.HTML(information.text, etree.HTMLParser())

    cities: List[etree.Element] = html.xpath('//div[@class="location-renderer__value"]')

    return cities[0].text


def get_weather(
    api_key: str, city: str, lang: str = "en", units: str = "metric"
) -> Dict:
    """
    Gets a json file that turns into a Dict
    with current weather information from openweather.
    """

    parameters: Dict[str, str] = {
        "appid": api_key,
        "q": city,
        "units": units,
        "lang": lang,
    }

    weather_information: requests.Response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather", params=parameters
    )

    return json.loads(weather_information.text)


def output_weather(api: str) -> None:
    """
    Output all the necessary information about the current weather
    in the region where your IP address is located to
    standard output.
    """

    info: Dict = get_weather(api, get_city())

    message: str = f"""\n\t\t[CURRENT FORECAST]
    
    {info['name']} pleases us with {info['main']['temp']} degrees Celsius
    on the street, which feels like {info['main']['feels_like']} degrees. 
    It is {info['weather'][0]['description']} outside now, 
    the wind is about {info['wind']['speed']} m/s, humidity is {info['main']['humidity']}%.\n"""

    print(message)


def main() -> None:
    """Takes API key form environment variables list. Starts output for weather."""

    output_weather(os.environ.get("API_OPENWEATHER"))


if __name__ == "__main__":
    main()
