from geopy.geocoders import Nominatim
from dadata import Dadata
from pprint import pprint
import envbox


SETTINGS_PREFIX = 'DADATA_'

env_all = envbox.get_environment()
env = env_all.getmany(SETTINGS_PREFIX)

print(env)

def get_setting(name: str) -> str:
    value = env.get(name)
    assert value, 'Укажите значение для настройки %s' % ('%s%s' % (SETTINGS_PREFIX, name))
    return value


class GeoLS:
  def __init__(self, _geols_name=None):
    self.geolocator = Nominatim(user_agent=_geols_name) #Указываем название приложения

  def get_loc(self):
    adress = str(input('Введите адрес: \n')) #Получаем интересующий нас адрес
    location = self.geolocator.geocode(adress) #Создаем переменную, которая состоит из нужного нам адреса
    # print(location) #Выводим результат: адрес в полном виде
    # print(location.latitude, location.longitude)
    data = {
        'adress': location.raw['display_name'],
        'coords': [location.latitude, location.longitude]
    }
    return data


class GeoLoc:
    def __init__(self, token=None):
        self.dadata = Dadata(token)

    def get_result(self):
        data = []
        adress = str(input('Введите адрес: \n'))  # Получаем интересующий нас адрес
        results = self.dadata.suggest("address", adress)
        for result in results:
            info_one = {'address': result['value'],
                        'okato': result['data']['okato'],
                        'oktmo': result['data']['oktmo'],
                        'coords': [result['data']['geo_lat'], result['data']['geo_lon']]
                        }
            data.append(info_one)
        return data


if __name__ == '__main__':
    geols = GeoLS('Tester')
    location = geols.get_loc()
    pprint(location)

    token = get_setting('TOKEN')
    geoloc = GeoLoc(token)
    data = geoloc.get_result()
    pprint(data)

