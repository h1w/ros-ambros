import requests
import base64

url = "http://tagproject.sfedu.ru/api/upload"

img = open("testimage.png", "rb").read()
img_64_encode = base64.encodebytes(img).decode()
payload = {
    "name": "Дима",
    "description": "Описание данной фотки, полный ужас, ямы повсюду, сделайте что-нибудь!!!",
    "gps": "41 24.2028, 2 10.4418",
    "image": img_64_encode,
    "request_type": "ambros",
}

r = requests.post(url, data=payload)