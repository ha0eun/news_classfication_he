import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split        # pip install scikit-learn
from konlpy.tag import Okt      # KoNLPy 설치하기 - 한글 형태소 분석기:: pip install konlpy
from keras_preprocessing.text import Tokenizer          # 형태소 단위로 나눠주는 것 설치하기 Okt(Open Korean Text): 형태소 분석기-- 토크나이징
from keras_preprocessing.sequence import pad_sequences    # pip install keras_preprocessing  # pip install tensorflow
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
import pickle

pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_columns', 15)
df = pd.read_csv('./crawling_data/naver_news_titles_20221124.csv')
df.category.replace('social', 'Social', inplace=True)
print(df.head(10))
print(df.category.value_counts())
df.info()

X = df['title']
Y = df['category']

encoder = LabelEncoder()
labeled_Y = encoder.fit_transform(Y)
print(labeled_Y[:5])
print(encoder.classes_)
with open('./models/label_encoder.pickle', 'wb') as f:      # encoder 저장하기 wb
    pickle.dump(encoder, f)
onehot_Y = to_categorical(labeled_Y)
print(onehot_Y[:5])

okt = Okt()

for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)       # 형태소를 자르고 원형으로 변형시켜줌(가다 == 갔으니 갔다 가므로 : 너무 많은 단어가 있어서
    if i % 100 == 0:
        print('.', end='')      # 100개 마다 '.' 찍기, 줄바꿈 X
    if i % 10000 == 0:
        print()

stopwords = pd.read_csv('./stopwords.csv', index_col=0)
for j in range(len(X)):         # len(X[:5] 슬라이싱[:5] 없애면 다 볼 수 있음
    words = []          # 빈 리스트
    for i in range(len(X[j])):           # len(X[j]) 0부터 시작
        if len(X[j][i]) > 1:            # len(X[j][i]) 형태소 길이가 하나 이상이면 words에 넣어줌
            if X[j][i] not in stopwords['stopword']:      # stopword(불용어) 리스트에 없으면 words에 넣어줌
                words.append(X[j][i])       # 한 글자, 불용어는 들어있지 않음
    X[j] = ' '.join(words)      # join 띄어쓰기 기준으로 하나로 이어 붙여서 하나의 문장으로 만듦
    #print(X[j])

token = Tokenizer()
token.fit_on_texts(X)       # X 안에 있는 형태소를 모두 뽑아서 유니크 형식으로 받음 / 형태소 마다 각 번호로 받음
tokened_X = token.texts_to_sequences(X)        # 순서대로 할때는 시퀀스를 사용한다
wordsize = len(token.word_index) + 1        # 형태소의 번호는 1부터 시작 (인덱스는 0이라서 +1)
with open('./models/news_token.pickle', 'wb') as f:         # 토큰 저장하기 wd
    pickle.dump(token, f)

# 제일 긴 문장의 길이에 맞춘다 -> 짧은문장 앞쪽 빈자리에 0을 붙여준다
max_len = 0
for i in range(len(tokened_X)):
    if max_len < len(tokened_X[i]):
        max_len = len(tokened_X[i])
print(max_len)

X_pad = pad_sequences(tokened_X, max_len)       # 앞에 0으로 패딩해서 가장 긴문장에 길이 맞춤

X_train, X_test, Y_train, Y_test = train_test_split(
    X_pad, onehot_Y, test_size=0.1)
print(X_train.shape, Y_train.shape, X_test.shape, Y_test.shape)

xy = X_train, X_test, Y_train, Y_test
np.save('./models/news_data_max_{}_wordsize_{}.npy'.format(max_len, wordsize), xy)      # xy에 저장