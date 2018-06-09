#!/usr/bin/python3
import re
import os
import argparse
import requests
from bs4 import BeautifulSoup


URL = r'http://www.randomtextgenerator.com/'
DATA = {
    'language': 'pl',
    'text_mode': 'plain'
}
HEADERS =  {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
    'Origin': 'http://www.randomtextgenerator.com',
    'Content-Type': 'application/x-www-form-urlencoded'
}


def generate_to_files(path: str, count: int):
    for i in range(count):
        print('Downloading {} file out of {}'.format(i + 1, count))
        res = requests.post(url=URL, data=DATA, headers=HEADERS)
        soup = BeautifulSoup(res.text, 'html.parser')
        random_text = soup.find('textarea').text
        filtered = '\n'.join(list(filter(lambda x: not re.match(r'^\s*$', x), random_text.split('\n'))))
        filename = 'generated_{}'.format(i)
        filepath = os.path.join(path, filename)
        with open(filepath, 'w') as file:
            file.write(filtered)
        print('Text saved in {}'.format(filepath))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dir")
    parser.add_argument("file_count")
    args = parser.parse_args()
    file_count = args.file_count
    base_path = os.path.abspath(args.dir)
    generate_to_files(base_path, int(file_count))
