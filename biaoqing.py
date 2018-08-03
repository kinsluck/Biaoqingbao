import os
import re
import time
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool, cpu_count


HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer': "http://www.fabiaoqing.com"
}


def makedir():
    today = time.strftime("%Y%m%d")
    if not os.path.exists(today):
        os.mkdir(today)
        os.chdir(today)
    else:
        os.chdir(today)


def save_pic(realbq_url, bq_name):
    img = requests.get(realbq_url, headers=HEADERS, timeout=10)
    with open(bq_name, 'ab') as f:
        f.write(img.content)
        print(bq_name)


def crawler(url):
    r = requests.get(url, headers=HEADERS).text
    img_infos = BeautifulSoup(r, 'lxml').find(
        'div', {'class': 'ui segment imghover'}).find_all('a')
    for img_info in img_infos:
        url_info = img_info.find('img', {'class': 'ui image lazy'})
        bq_name = url_info['title']
        realbq_url = url_info['data-original']
        realbq_url = re.sub('bmiddle', 'large', realbq_url)
        suffix = re.search(
            'jpg|bmp|gif|ico|pcx|jpeg|tif|png|raw|tga', realbq_url).group()
        bq_name += '.'+suffix
        save_pic(realbq_url, bq_name)


if __name__ == '__main__':
    makedir()
    bq_url = [
        'http://fabiaoqing.com/biaoqing/lists/page/{cnt}.html'.format(cnt=cnt)
        for cnt in range(0, 6)]
    pool = Pool(processes=cpu_count())
    pool.map(crawler, bq_url)
