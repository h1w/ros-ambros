import requests
import base64

url = "http://tagproject.sfedu.ru/map/api/upload"

img = open("testimage.png", "rb").read()
img_64_encode = base64.encodebytes(img).decode()
payload = {
    "name": "aboba",
    "description": "aboba aboba aboba...",
    "gps": "47.2177, 39.0248",
    "image": img_64_encode,
    "request_type": "road",
}

response = requests.post(url, data=payload, verify=False)