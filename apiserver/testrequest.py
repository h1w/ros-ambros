import requests
url = "http://tagproject.sfedu.ru/api/upload"
img = {
    "image": open("testimage.png", "rb")
}
payload = {
    "name": "Дима",
    "description": "Описание данной фотки, полный ужас, ямы повсюду, сделайте что-нибудь!!!",
    "gps": "41 24.2028, 2 10.4418"
}
r = requests.post(url, files=img, data=payload)

# convert server response into JSON format
print(r.json())