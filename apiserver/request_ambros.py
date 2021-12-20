import requests
import base64

url = "http://tagproject.sfedu.ru/api/upload"

img = open("1.jpg", "rb").read()
img_64_encode = base64.encodebytes(img).decode()
payload = {
    "name": "Дмитрий",
    "description": "Много амброзии, сделайте что-нибудь!",
    "gps": "47.6159, 38.9115",
    "image": img_64_encode,
    "request_type": "ambros",
}

r = requests.post(url, data=payload)