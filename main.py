from sys import argv
from datetime import date, timedelta, datetime
from WeatherData import WeatherForecast

if __name__ == '__main__':
    wf = WeatherForecast(argv[1])

    if len(argv) >= 3:
        checkDate = date.fromisoformat(argv[2])
    else:
        checkDate = date.today() + timedelta(days=1)

    # for testing
    print('items:')
    for item in wf.items():
        print(item[0], item[1])
    result = wf[checkDate.strftime('%Y-%m-%d')]
    print('pogoda na:', result['dt'], result['weather_description'])

