import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split        # pip install scikit-learn
from konlpy.tag import Okt      # KoNLPy 설치하기 - 한글 형태소 분석기:: pip install konlpy
from keras_preprocessing.text import Tokenizer          # 형태소 단위로 나눠주는 것 설치하기 Okt(Open Korean Text): 형태소 분석기-- 토크나이징
from keras_preprocessing.sequence import pad_sequences    # pip install keras_preprocessing  # pip install tensorflow
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
import pickle
from keras.models import load_model

pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_columns', 15)
df = pd.read_csv('./crawling_data/naver_headline_news_20221128.csv')
print(df.head())
df.info()

X = df['title']
Y = df['category']

# 엔코딩할때 같은 모델로 사용해야함! 새로 만들지 말고 있던 걸 쓰기!
with open('./models/label_encoder.pickle', 'rb') as f: # rb 읽어오기
    encoder = pickle.load(f)    # 읽어올때는 load
labeled_Y = encoder.transform(Y)
onehot_Y = to_categorical(labeled_Y)

okt = Okt()
for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)
stopwords = pd.read_csv('./stopwords.csv', index_col=0)
for j in range(len(X)):
    words = []
    for i in range(len(X[j])):
        if len(X[j][i]) > 1:
            if X[j][i] not in list(stopwords['stopword']):
                words.append(X[j][i])
    X[j] = ' '.join(words)

with open('./models/news_token.pickle', 'rb') as f:
    token = pickle.load(f)
tokened_X = token.texts_to_sequences(X)
for i in range(len(tokened_X)):
    if len(tokened_X[i]) > 20:      # 모델이 입력을 20개만 줌
        tokened_X[i] = tokened_X[i][:20]    # 형태소가 20자 보다 많다면 버려라
X_pad = pad_sequences(tokened_X, 20)        # 모델링 할때 데이터 정보가 없으면 0으로 나타냄

model = load_model('./models/news_category_classfication_model_0.994.h5')
preds = model.predict(X_pad)
label = encoder.classes_
category_preds = []
for pred in preds:
    category_pred = label[np.argmax(pred)]  # 가장 큰값의 인덱스를 나타냄
    category_preds.append(category_pred)
df['predict'] = category_preds

# print(df.head(30))

df['OX'] = False
for i in range(len(df)):
    if df.loc[i, 'category'] == df.loc[i, 'predict']:
        df.loc[i, 'OX'] = True

print(df.head(30))
print(df['OX'].value_counts())
print(df['OX'].mean())
print(df.loc[df['OX']==False])