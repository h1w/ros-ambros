import requests
import base64

url = "http://tagproject.sfedu.ru/map/api/upload"

# headers = {
#     'accept': 'text/html,application/xhtml+xml,application/xml',
#     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
# }

# response = requests.get(url, headers=headers, verify=False)

# headers['cookie'] = '; '.join([x.name + '=' + x.value for x in response.cookies])
# headers['content-type'] = 'application/x-www-form-urlencoded'

# print(headers)

img = open("testimage.png", "rb").read()
img_64_encode = base64.encodebytes(img).decode()
payload = {
    "name": "aboba",
    "description": "aboba aboba aboba...",
    "gps": "47.2177, 39.0248",
    "image": img_64_encode,
    "request_type": "road",
}

# response = requests.post(url, data=payload, headers=headers, verify=False)

response = requests.post(url, data=payload, verify=False)

# print('\n\n\n',  headers)