import vk_api
import json
import requests
import urllib3
import schedule
import telebot
from telebot.types import InputMediaPhoto
import time
from utils import get_vk_photo
from const import login, password, token

bot = telebot.TeleBot(token=token)

s = requests.Session()

vk_session = vk_api.VkApi(login, password)

try:
    vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)

vk = vk_session.get_api()


def vk_get():
    response_photo = vk.photos.get(owner_id=-1881436, album_id='wall', rev=False, count=350)
    response_gif = ''
    response_video = ''
    num = 0
    # post = response['items'][0]['attachments']
    identif = response_photo['items'][num]['id']

    response = vk.wall.get(owner_id=-1881436)

    with open("lastkey.txt", "r") as  f:
        lastkey = f.read()
    lastkey = int(lastkey)
    if identif > lastkey:
        json_maspho = response_photo['items'][num]
        biba = 'post_id' in json_maspho
        text = response['items'][1]['text']
        if biba == True:
            json_maspho = response_photo['items'][0]['sizes']

            print(len(json_maspho))
            post = (json_maspho[-1])
            print(text)
            url = post['url']

            with open('vk.jpg', 'wb') as f:
                response = s.get(url, stream=True)

                for block in response.iter_content(1024):
                    if not block:
                        break

                    f.write(block)

            photo = open('vk.jpg', 'rb')
            if len(text) == 0:
                bot.send_photo(-1001310642208, photo)
            else:
                bot.send_photo(-1001310642208, photo, caption=text)

        if biba == False:
            msgs = []
            for i in range(num, 50):
                json_maspho = response_photo['items'][i]
                biba = 'post_id' in json_maspho
                if biba == False:
                    json_masphos = response_photo['items'][i]['sizes']
                    post = (json_masphos[-1])
                    url = post['url']
                    msgs.append(url)
                    print(i)

                if biba == True:
                    break

            print(msgs)
            n = 0
            for url in msgs:
                vk_name = 'vk'
                n = str(n)
                print('n в начале цикла:', n)
                print('vk в начале цикла:', vk_name)
                vk_name += n
                with open(vk_name + '.jpg', 'wb') as f:
                    response = s.get(url, stream=True)

                    for block in response.iter_content(1024):
                        if not block:
                            break

                        f.write(block)
                n = int(n)
                n = n + 1
            n = 0
            photos = []
            for photo in range(len(msgs)):
                vk_name = 'vk'
                n = str(n)
                print('n в начале цикла:', n)
                print('vk в начале цикла:', vk_name)
                vk_name += n
                photo = open(vk_name + '.jpg', 'rb')
                photos.append(photo)
                n = int(n)
                n = n + 1
            if len(text) == 0:
                bot.send_media_group(-1001310642208, [InputMediaPhoto(photo) for photo in photos])
            else:
                bot.send_media_group(-1001310642208, [InputMediaPhoto(photo) for photo in photos], caption=text)

        with open("lastkey.txt", "w") as f:
            f.write(str(identif))


schedule.every(60).seconds.do(vk_get)

while True:
    schedule.run_pending()
    time.sleep(1)
