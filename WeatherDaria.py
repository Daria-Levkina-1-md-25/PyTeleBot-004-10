from pyowm.utils.config import get_default_config
from pyowm import OWM
import configparser
import pyowm

def location(message):
    config_dict=get_default_config()
    config_dict['language'] = 'ru'
    try:
        if message.location is not None:
            lat = message.location.latitude
            lon = message.location.longitude
            owm = pyowm.OWM('e16df7abec8b90246e3f87cfba41636c')
            mgr = owm.weather_manager()
            one_call = mgr.one_call(lat=lat, lon=lon)
            observation = mgr.weather_at_coords(lat, lon)
            w = observation.weather
            wind = w.wind()['speed']
            humi = w.humidity
            rain = w.rain
            snow = w.snow
            st = w.status
            dt = w.detailed_status
            ti = w.reference_time('iso')
            pr = w. pressure['press']
            vd = w.visibility_distance
            t = w.temperature("celsius")
            t1= t['temp_max']

            weather1 = one_call.forecast_daily[0].temperature('celsius').get('morn', None)
            weather_text = "Максимальная температура: " + str(t1) + '\n' + \
                             "Средняя температура за день = " + str(weather1) + '\n' + \
                             'Скорость ветра: '+ str(wind) + 'M/c'+ '\n' + \
                             "Давление: " + str(pr)+ "мм.рт.ст" + '\n' \
                             "Влажность: " + str(humi) + "%" + '\n' \
                             "Видимость: " + str(vd) + " метров" + '\n' \
                             "Статус: " + str(st) + '\n' + str(dt)+ '\n' \
                             "Дождь: " + str(rain) + '\n' \
                             "Снег: " + str(snow) + '\n' \
                             "Сейчас: " + str(ti)

            return weather_text
    except Exception:
        error_text = "Прости, произошла ошибка."
        return error_text