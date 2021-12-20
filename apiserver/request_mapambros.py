import requests
import base64

url = "http://tagproject.sfedu.ru/map/api/upload"

img = open("5.jpg", "rb").read()
img_64_encode = base64.encodebytes(img).decode()
payload = {
    "name": "Дмитрий",
    "description": "Куда смотрит администрация! Густые заросли амброзии!!!",
    "gps": "47.2315, 38.86748",
    "image": img_64_encode,
    "request_type": "ambros",
}

response = requests.post(url, data=payload, verify=False)