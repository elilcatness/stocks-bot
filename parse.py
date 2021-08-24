import json
import os

import requests
from json.decoder import JSONDecodeError

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/91.0.4472.124 Safari/537.36'}


def get_stocks_percents(url):
    response = requests.get(url, headers={**HEADERS, 'x-xsrf-token': os.getenv('x-xsrf-token'),
                                          'cookie': os.getenv('cookie')})
    if not response:
        print(response.text)
        return print(f'Failed to get JSON from {url}')
    try:
        with open('response.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(response.json(), indent=4, ensure_ascii=False))
        data = response.json()['data']
    except JSONDecodeError:
        return print(f'Failed to decode a JSON received from {url}')
    return [tuple(item.values()) for item in data]