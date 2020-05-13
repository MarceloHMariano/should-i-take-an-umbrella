import argparse
from typing import List, Optional

import pyowm
from pyowm.weatherapi25.forecast import Forecast
from pyowm.weatherapi25.weather import Weather


def parse_command_line_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    args_group = parser.add_argument_group(title='required arguments')
    args_group.add_argument('--api-key',
                            required=True,
                            type=str,
                            dest='api_key',
                            metavar='<API_KEY>',
                            help='OpenWeatherMap API KEY')

    args_group.add_argument('--city',
                            required=True,
                            type=str,
                            dest='city',
                            metavar='<CITY>',
                            help="The city's name")

    return parser.parse_args()


def get_five_day_forecast(city: str, api_key: str) -> Forecast:
    api_client = pyowm.OWM(api_key)
    forecaster = api_client.three_hours_forecast(city)
    return forecaster.get_forecast()


def get_forecast_latest_weathers(forecast: Forecast) -> List[Weather]:
    weathers = {}

    for weather in forecast.get_weathers():
        weather_date = weather.get_reference_time('date').strftime('%Y-%M-%d')
        weathers[weather_date] = weather

    return list(weathers.values())


def get_humid_days(city: str, api_key: str) -> List[str]:
    forecast = get_five_day_forecast(city, api_key)
    weathers = get_forecast_latest_weathers(forecast)

    humid_days = []

    for weather in weathers:
        if weather.get_humidity() > 70:
            day = weather.get_reference_time('date').strftime('%A')
            humid_days.append(day)

    return humid_days


def format_humid_days(humid_days: List[str]) -> Optional[str]:
    if len(humid_days) == 0:
        return None

    if len(humid_days) == 1:
        return humid_days[0]

    return f'{", ".join(humid_days[:-1])} and {humid_days[-1]}.'


def main() -> None:
    args = parse_command_line_args()

    humid_days_list = get_humid_days(args.city, args.api_key)
    humid_days = format_humid_days(humid_days_list)

    if humid_days is not None:
        print(f'You should take an umbrella in these days: {humid_days}')


if __name__ == '__main__':
    main()
