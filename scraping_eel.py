import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

list_df = pd.DataFrame(columns=['店舗名', '口コミ'])

name_list = []
link_list = []

# 店舗一覧ページ
for page in range(1, 30):
    url = 'https://tabelog.com/fukuoka/rstLst/unagi/' + str(page) + '/?svd=20191026&svt=1900&svps=2'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    # 店舗一覧ページから店舗名一覧と店舗詳細ページのリンクを取得
    store_tags = soup.find_all('a', class_='list-rst__rst-name-target cpy-rst-name')
    for store_tag in store_tags:
        # 店舗詳細ページのリンクが格納されたリスト作成
        link_list.append(store_tag.get('href'))
        # 店舗名一覧が格納されたリスト作成
        store_name = store_tag.text
        store_name = store_name.replace('　', '')
        store_name = store_name.replace(' ', '')
        name_list.append(store_name)

    for store_name, link in zip(name_list, link_list):
        # 店舗詳細ページ
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'lxml')
        # 店舗詳細ページから口コミ一覧ページへのリンクを取得
        review_tag_id = soup.find('li', id='rdnavi-review')
        review_tag_href = review_tag_id.a.get('href')

        # 口コミ一覧ページ
        response = requests.get(review_tag_href)
        soup = BeautifulSoup(response.text, 'lxml')
        # 口コミ一覧ページから口コミ詳細ページへのリンク取得
        review_comments = soup.find_all('a', class_='rvw-item__title-target')
        for review_comment in review_comments:

            # 口コミ詳細ページ
            response = requests.get('https://tabelog.com' + review_comment.get('href'))
            soup = BeautifulSoup(response.text, 'lxml')
            # 口コミ取得
            review_tags = soup.find_all('div', class_='rvw-item__rvw-comment')
            review = review_tags[0].p.text.encode('cp932', 'ignore')
            review = review.decode('cp932')
            review = review.replace('\n','')
            review = review.replace(' ','')
            review = review.replace('　','')

            # サーバーに負荷を与えないため1秒待機
            time.sleep(1)

            # 取得した項目
            # store_name=店舗名
            # review=口コミ
            tmp_se = pd.DataFrame([store_name, review], index=list_df.columns).T
            list_df = list_df.append(tmp_se)

print(list_df)

# CSV保存
list_df.to_csv('list_eel.csv', mode = 'a', encoding='cp932')