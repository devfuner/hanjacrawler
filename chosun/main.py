
# 교육 취업 - 신문은 선생님
# http://news.chosun.com/svc/list_in/list.html?catid=B2


import os
import shutil

import requests
from bs4 import BeautifulSoup


UTF_8 = 'utf-8'
EUC_KR = 'euc-kr'


def fetch(url, encoding=None):
    """
    url에 해당하는 html text를 반환하는 함수

    :param encoding: utf-8, euc-kr
    :param url:
    :return:
    """
    response = requests.get(url)
    if encoding:
        response.encoding = encoding

    return response.text


def find_title(markup):
    """
    '신문은 선생님'의 목록에서 '[신문으로 배우는 실용한자]'만 필터링 한다.

    :param markup:
    :return:
    """
    soup = BeautifulSoup(markup, 'html.parser')
    a_tags = soup.find_all('a')
    titles = []

    for a in a_tags:
        if a.has_attr('href'):
            title = str(a.string)
            if title.startswith('[신문으로 배우는 실용한자]'):
                print('수집대상 url :', a['href'])
                print('수집대상 title :', title)
                titles.append(a['href'])

    return titles


def find_image(markup):
    """
    markup에서 img 태그를 찾아서 src 속성의 값을 반환한다.

    :param markup:
    :return:
    """
    soup = BeautifulSoup(markup, 'html.parser')
    img = soup.img

    return img['src']


def download_item(url):
    """
    이미지 url을 다운로드 받는다.

    :param url:
    :return:
    """
    print('download :', url)
    basename = os.path.basename(url)
    print('basename :', basename)
    filename, ext = os.path.splitext(basename)

    data = requests.get(url, stream=True)
    data.raw_decode_content = True

    with open(filename + ext, 'wb') as f:
        shutil.copyfileobj(data.raw, f)


def crawler():
    pass


if __name__ == '__main__':
    # 목록 URL
    # pn 페이지 번호
    list_url = 'http://news.chosun.com/svc/list_in/list.html?catid=B2&pn={page}'
    formatted_url = list_url.format(page=2)

    titles = find_title(fetch(formatted_url, UTF_8))

    for item in titles:
        # item url ex : http://news.chosun.com/site/data/html_dir/2018/08/03/2018080300087.html
        markup = fetch(item, UTF_8)
        image_url = find_image(markup)
        download_item(image_url)
