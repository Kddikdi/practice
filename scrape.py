import urllib.request
from bs4 import BeautifulSoup
import json
import requests

# アクセス先urlとUAを設定
url = 'https://news.yahoo.co.jp/topics'
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) '\
     'AppleWebKit/537.36 (KHTML, like Gecko) '\
     'Chrome/67.0.3396.99 Safari/537.36 '
# 記事取得関数


def getNews(word):

    # 下記はアクセス先に合わせて修正しスクレイピング
    req = urllib.request.Request(url, headers={'User-Agent': ua})
    html = urllib.request.urlopen(req)
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find('div', attrs={'class': 'sc-jtRfpW dYgtLJ'})
    topics = main.select("li > a")

    # 該当記事カウント変数と結果格納リスト
    count = 0
    list = []

    # スクレイピング結果から引数wordを含む記事を結果リストに格納
    for topic in topics:
        if topic.contents[0].find(word) > -1:
            list.append(topic.contents[0])
            list.append(topic.get('href'))
            count += 1
    if count == 0:
        list.append("該当記事はありません")

    # リスト内の要素間に改行を挿入して返却
    result = '\n'.join(list)
    return result
