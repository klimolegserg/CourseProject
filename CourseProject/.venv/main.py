import requests
import json
from pprint import pprint
import logging

logging.basicConfig(level=logging.INFO, filename='py_log.log', filemode='w')
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")

from urllib.parse import urlencode

# чтение из файла токена яндекс диска, сам файл добавлен в gitignore
with open('token.txt') as f:
   key = f.readline()

base_url = 'https://cloud-api.yandex.net'

# Создание папки на яндекс диске
# url_create_folder = base_url + '/v1/disk/resources'
# params_dict = {
#     'path': 'photo_from_vk'
# }
# headers_dict = {
#     'Authorization': key
# }
#
# response = requests.put(url_create_folder, params=params_dict, headers=headers_dict)
#
# print(response.status_code)
# pprint(response.json())

url_get_link = base_url + '/v1/disk/resources/upload'
params_dict = {
    'path': 'photo_from_vk/'
}
headers_dict = {
    'Authorization': key
}

response = requests.put(url_get_link, params=params_dict, headers=headers_dict)
pprint(response.status_code)
pprint(response.json())

url_for_upload = response.json().get('href')


# Получение VK Token

# APP_ID = '51818380'
# OAUTH_BASE_URL = 'https://oauth.vk.com/authorize'
# params = {'client_id': APP_ID,
#     'redirect_uri': 'https://oauth.vk.com/blank.html',
#     'scope': 'photos',
#     'display': 'page',
#     'response_type': 'token'
# }
#
# OAUTH_URL = f'{OAUTH_BASE_URL}?{urlencode(params)}'
# print(OAUTH_URL)


def get_photo_from_vk() -> list:
# Чтение VKToken из файла, сам файла добавлен в gitignore
   with open('tokenVK.txt') as f:
      token = f.readline()

   params = {'access_token': token, 'v': '5.199', 'owner_id': '838612895', 'album_id': 'profile', 'rev': '0', 'extended': '1', 'count': '5'}
   response = requests.get('https://api.vk.com/method/photos.getAll', params=params)
   pprint(response.status_code)
   pprint(response.json())

   global list_photo
   list_photo = []
   photos_dict = {}
   size_dict = {'size': 'z'}
   for photo in response.json():
      if photo['items']['sizes']['type'] == 'w':
         photo_name = photo['items']['date'] + photo['items']['likes']['count']
         photo_url = photo['items']['sizes']['url']
         res = requests.get(photo_url)
         with open(f'{photo_name}.jpg', 'wb') as file:
            file.write(res.content)
            photos_dict.setdefault('file_name', f"{photo_name}.jpg")
            photos_dict.update(size_dict)
            list_photo.append(photos_dict)
   return list_photo


get_photo_from_vk()

with open('foto.json', 'w') as f:
   json.dump(list_photo, f)
with open('foto.json', 'rb') as file:
   response = requests.put('url_for_upload', files={'file': file}, headers=headers_dict)
   print(response.status_code)











