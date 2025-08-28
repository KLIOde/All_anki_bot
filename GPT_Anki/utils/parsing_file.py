import requests
Api_token = '6ac8cff694a46392fa58a4d69dbc0a8a'
word = 'literacy'
url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

response = requests.get(url)
if response:
    x = response.json()
    print(x)
