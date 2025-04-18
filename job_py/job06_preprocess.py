import pickle
import pandas as pd
import numpy as np
from pygments.lexer import words
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt, Komoran
from sklearn.preprocessing import  LabelEncoder
from keras.utils import to_categorical
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re


df = pd.read_csv('../crawling_data/news_titles.csv')
df.info()
# print(df.head(30))
# print(df.category.value_counts())

x = df.titles
y = df.category

# print(x[1])
okt = Okt()

# okt_x = okt.morphs(x[1])
# print(okt_x)
# okt_x = okt.morphs(x[1], stem=True)
# print(okt_x)
#
# komoran = Komoran()
# komoran_x = komoran.morphs(x[0])
# print(komoran_x)

encoder = LabelEncoder()
labeled_y = encoder.fit_transform(y)
print(labeled_y[:5])
label = encoder.classes_
print(label)
with open('../models/encoder.pickle', 'wb') as f: #피클은 데이터가 뭐가 됐든 숫자로 저장
    pickle.dump(encoder, f)

onehot_y = to_categorical(labeled_y)
print(onehot_y)

# cleaned_x = re.sub('[^가-힣]', ' ', x[1]) #한글만 남기고
# print(x[1])
# print(cleaned_x)

for i in range(len(x)):
    x[i] = re.sub('[^가-힣]', ' ', x[i])
    x[i] = okt.morphs(x[i], stem=True)
    if i % 1000 == 0:
        print(i)
print(x)
for idx, sentence in enumerate(x):
    words = []
    for word in sentence:
        if len(word) > 1:
            words.append(word)
    x[idx] = ' '.join(words) #띄어쓰기 기준으로 재정렬

print(x[:10])

token = Tokenizer() # 형태소에 숫자 라벨 붙이는 작업 (꽃샘추위 7, 대학 13, 신자 20)
token.fit_on_texts(x)
tokened_x = token.texts_to_sequences(x)
print(tokened_x)
wordsize = len(token.word_index) + 1
print(wordsize)

max = 0
for sentence in tokened_x:
    if max < len(sentence):
        max = len(sentence)
print(max)

with open('./models/token_max{}.pickle'.format(max), 'wb') as f:
    pickle.dump(token, f)

# 데이터 길이 맞추기 가장 긴 문장을 찾아서 길이를 찾고
# 나머지 문장들에게 0을 입력

x_pad = pad_sequences(tokened_x, max) # 길이 맞춰주는 함수
print(x_pad)

x_train, x_test, y_train, y_test = train_test_split(
    x_pad, onehot_y, test_size=0.1)
print(x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)

np.save('./crawling_data/title_x_train_wordszie{}'.format(wordsize),x_train)
np.save('./crawling_data/title_x_test_wordszie{}'.format(wordsize),x_test)
np.save('./crawling_data/title_y_train_wordszie{}'.format(wordsize),y_train)
np.save('./crawling_data/title_y_test_wordszie{}'.format(wordsize),y_test)

