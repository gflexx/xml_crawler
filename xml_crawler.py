from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from pathlib import Path
import requests
import os

url = "https://storage.googleapis.com/wineshop-assets"
base_dir = Path(__file__).resolve().parent

def main(url):
    page = urlopen(url)
    if page:
        print('Opening page OK!\n')
    else:
        print('Something went wrong...')

    print('Reading data...\n')
    xml_ = page.read().decode('utf-8')
    soup = bs(xml_, 'xml')

    # get image urls from xml
    print('Extracting data..\n')
    file_list = []
    pic_list = soup.find_all('Key')
    for item in pic_list:
        file_list.append(item.get_text())
        print(item.get_text())

    # remove last non image value
    file_list.pop()

    # setting img path
    if not os.path.exists('imgs'):
        os.makedirs('imgs')
    _path = os.path.join(base_dir, 'imgs')

    # get image from urls
    print('\nDownloading images...\n')
    for item in file_list:
        filename = item.split("/")[-1]

        img_url = url + '/' + item
        response = requests.get(img_url)
        print('Getting ', filename, ' Ok!')

        # write file
        path = _path + '/' + filename
        file = open(path, 'wb')
        file.write(response.content)
        file.close()

    print('\nDone!')


if __name__ == '__main__':
    main(url)
