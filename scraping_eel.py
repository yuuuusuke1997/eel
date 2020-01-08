import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

list_df = pd.DataFrame(columns=['店舗名', '口コミ'])

name_list = []
link_list = []

#  store list page
for page in range(1, 30):
    url = 'https://tabelog.com/fukuoka/rstLst/unagi/' + str(page) + '/?svd=20191026&svt=1900&svps=2'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    # get store names list and link of store details page
    store_tags = soup.find_all('a', class_='list-rst__rst-name-target cpy-rst-name')
    for store_tag in store_tags:
        # make list that stored store details pages
        link_list.append(store_tag.get('href'))
        # make list that stored store names
        store_name = store_tag.text
        store_name = store_name.replace('　', '')
        store_name = store_name.replace(' ', '')
        name_list.append(store_name)

    for store_name, link in zip(name_list, link_list):
        #  store details page
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'lxml')
        # get link of review list page
        review_tag_id = soup.find('li', id='rdnavi-review')
        review_tag_href = review_tag_id.a.get('href')

        # review list page
        response = requests.get(review_tag_href)
        soup = BeautifulSoup(response.text, 'lxml')
        # get link of review details page
        review_comments = soup.find_all('a', class_='rvw-item__title-target')
        for review_comment in review_comments:

            # review details page
            response = requests.get('https://tabelog.com' + review_comment.get('href'))
            soup = BeautifulSoup(response.text, 'lxml')
            # get reviews
            review_tags = soup.find_all('div', class_='rvw-item__rvw-comment')
            review = review_tags[0].p.text.encode('cp932', 'ignore')
            review = review.decode('cp932')
            review = review.replace('\n','')
            review = review.replace(' ','')
            review = review.replace('　','')

            time.sleep(1)

            tmp_se = pd.DataFrame([store_name, review], index=list_df.columns).T
            list_df = list_df.append(tmp_se)

print(list_df)

list_df.to_csv('list_eel.csv', mode = 'a', encoding='cp932')