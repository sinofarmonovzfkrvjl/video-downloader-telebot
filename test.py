import requests

def test():
    response = requests.get("https://full-media-downloader-pro-zfkrvjl323.onrender.com/youtube1", params={"url": "https://youtu.be/qEJ4hkpQW8E-", "token": open("token.txt", 'r').read()})
    print(response.json())

test()
