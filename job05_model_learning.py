import numpy as np
import matplotlib.pyplot as plt
from keras.models import *
from keras.layers import *

X_train, X_test, Y_train, Y_test = np.load(
    './models/news_data_max_20_wordsize_11919.npy', allow_pickle=True)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

model = Sequential()
model.add(Embedding(11919, 300, input_length=20))   # (단어수, 몇 차원의 수, max_len 길이) 받은 데이터의 단어의 수와 일치해야함!
        # 인간의 자연어는 수치화되어 있지 않은 데이터이기 때문에 수치화 해야함.'언어의 벡터화'가 이뤄지고, 일련의 과정을 Word Embedding
model.add(Conv1D(32, kernel_size=5, padding='same', activation='relu'))  # 1차원
model.add(MaxPool1D(pool_size=1))   # pool_size=1 이면 다름이 없지만 써줌!
model.add(GRU(128, activation='tanh', return_sequences=True))
model.add(Dropout(0.3))
model.add(GRU(64, activation='tanh', return_sequences=True))
model.add(Dropout(0.3))
model.add(GRU(64, activation='tanh'))
model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(6, activation='softmax'))  # 카테고리가 6개- 뉴스 카테고리
model.summary()

model.compile(loss='categorical_crossentropy', optimizer='adam',
              metrics=['accuracy'])
fit_hist = model.fit(X_train, Y_train, batch_size=128, epochs=10,
                     validation_data=(X_test, Y_test))
model.save('./models/news_category_classfication_model_{}.h5'.format(
    np.round(fit_hist.history['val_accuracy'][-1], 3)))
plt.plot(fit_hist.history['accuracy'], label='accuracy')
plt.plot(fit_hist.history['val_accuracy'], label='val_accuracy')
plt.legend()
plt.show()






