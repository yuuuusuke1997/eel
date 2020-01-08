from janome.tokenizer import Tokenizer
from gensim.models import word2vec
import pandas as pd

df_file = pd.read_csv('list_eel.csv', encoding='cp932')

store_names = df_file['店舗名'].tolist()
reviews = df_file['口コミ'].tolist()

t = Tokenizer()

result = []

for i, review in enumerate(reviews):
    s = review
    tokens = t.tokenize(s)

    r = []

    for tok in tokens:
        if tok.base_form == '*':
            word = tok.surface
        else:
            word = tok.base_form

        ps = tok.part_of_speech

        hinshi = ps.split(',')[0]

        if hinshi in ['名詞', '形容詞', '動詞']:
            r.append(word)

    rl = (' '.join(r)).strip()
    result.append(store_names[i])
    result.append(rl)
    result = [i.replace('\u3000','') for i in result]

print(result)

text_file = 'wakati_list_eel.txt'
with open(text_file, 'w', encoding='utf-8') as fp:
    fp.write("\n".join(result))

data = word2vec.LineSentence(text_file)
model = word2vec.Word2Vec(data, size=200, window=1, hs=1, min_count=1, sg=1)
model.save('./wakati_list_eel.model')