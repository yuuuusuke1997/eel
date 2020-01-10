from gensim.models import word2vec
import pandas as pd

model = word2vec.Word2Vec.load('./wakati_list_eel.model')

df_file = pd.read_csv('list_eel.csv', encoding='cp932')
store_names = df_file['店舗名'].tolist()

# Any store name
keyword = '富松うなぎ屋黒田本店'

dic = {}

for store_name in store_names:
    result = model.wv.similarity(store_name, keyword)

    dic[store_name] = result

# get 5 store with similarity to your input the store
result = sorted(dic.items(), key=lambda x: -x[1])[1:6]
print(result)