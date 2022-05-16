"""
Output all the necessary information about the current weather
in the region where your IP address is locate.
"""

import os
import json
from typing import List, Dict
from sys import argv

import requests
from lxml import etree


def get_city() -> str:
    """
    Gets name of your city by IP address
    from yandex.ru/internet.

    :return: name of city
    """

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

    :param api_key: api key from open weather for accessing information
    :param city: place where will check the current weather
    :param lang: output information in json will be in this language
    :param units: in general, Celsius ("metric") is used for temperature
    :return: current weather in Dict

    For more information check API documentation OpenWeather.
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


def output_weather(api: str, file) -> None:
    """
    Output all the necessary information about the current weather
    in the region where your IP address is located to
    standard output or a file that is entered as an optional
    argument.

    >> python3 weather.py filename.txt

    In general, it seems like that:
    >> python3 [programme name] [file for output]


    :param api: api key from OpenWeather
    :param file: optional argument for output
    :return: output information in file or stdout
    """

    info: Dict = get_weather(api, get_city())

    message: str = f"""\n\t\t[CURRENT FORECAST]
    
    {info['name']} pleases us with {info['main']['temp']} degrees Celsius
    on the street, which feels like {info['main']['feels_like']} degrees. 
    It is {info['weather'][0]['description']} outside now, 
    the wind is about {info['wind']['speed']} m/s, humidity is {info['main']['humidity']}%.\n"""

    if file is not None:
        with open(file, "w", encoding="utf-8") as writer:
            writer.write(message)
    else:
        print(message)


def main() -> None:
    """
    Gets argv from input and take API key form environment variables list.
    Starts output for weather.

    >> python3 [programme name].py [arg1] [arg2] ... [argN]
    :return: None
    """

    output_file = None
    if len(argv) >= 2:
        output_file = argv[1]

    output_weather(os.environ.get("API_OPENWEATHER"), output_file)


if __name__ == "__main__":
    main()
