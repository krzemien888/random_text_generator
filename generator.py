#!/usr/bin/python3
import re
import os
import argparse
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool


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


def save_to_file(path: str, content: str, times: int):
    repeated_content = '\n'.join(content for _ in range(times))
    with open(path, 'a') as file:
        file.write(repeated_content)
    print('Text saved in {}'.format(path))


def generate_to_files(path: str, count: int, repeat: int):
    files_content = []
    for i in range(count):
        print('Downloading {} file out of {}'.format(i + 1, count))
        res = requests.post(url=URL, data=DATA, headers=HEADERS)
        soup = BeautifulSoup(res.text, 'html.parser')
        random_text = soup.find('textarea').text
        filtered = '\n'.join(list(filter(lambda x: not re.match(r'^\s*$', x), random_text.split('\n'))))
        filename = 'generated_{}.txt'.format(i)
        filepath = os.path.join(path, filename)
        files_content.append((filepath, filtered))
    with Pool(processes=8) as p:
        for filepath, content in files_content:
            p.apply_async(save_to_file, (filepath, content, repeat))
        p.close()
        p.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dir")
    parser.add_argument("file_count")
    parser.add_argument("append_repeat")
    args = parser.parse_args()
    file_count = args.file_count
    append_repeat = args.append_repeat
    base_path = os.path.abspath(args.dir)
    generate_to_files(base_path, int(file_count), int(append_repeat))
