from threading import activeCount

import numpy as np
import matplotlib.pyplot as plt
from keras.models import *
from keras.layers import *

x_train = np.load('./crawling_data/title_x_train_wordszie15396.npy', allow_pickle=True)
x_test = np.load('./crawling_data/title_x_test_wordszie15396.npy', allow_pickle=True)
y_train = np.load('./crawling_data/title_y_train_wordszie15396.npy', allow_pickle=True)
y_test = np.load('./crawling_data/title_y_test_wordszie15396.npy', allow_pickle=True)
print(x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)

model = Sequential()
model.add(Embedding(15396, 300)) # 형태소 15396 의미공간상 차원의 벡터화, 15396 형태소에 대해 좌표값이 생성
#300 = 300차원으로 축소 이유는 차원의 저주 = 희소해진다 = 빈 공강이 생김 즉 학습이 안됨, 사진, 큐브, 데이터 손실을 최소화시키며 300차원으로 줄인다
model.build(input_shape=(None, 25))
model.add(Conv1D(32, kernel_size=5, padding='same', activation='relu')) # 이미지는 2D, 문장은 1D(단어니까)
model.add(MaxPool1D(pool_size=1)) #의미는 없지만 컨브레이어 뒤에는 항상 붙음
model.add(LSTM(128, activation='tanh', return_sequences=True)) # RNN은 긴 문장에는 학습이 안됨
model.add(Dropout(0,3))                # return_sequences=True 반복되는 값을 저장 뒤에 LSTM이 있으면 있어야함
model.add(LSTM(64, activation='tanh', return_sequences=True))
model.add(Dropout(0,3))
model.add(LSTM(64, activation='tanh'))
model.add(Dropout(0,3))
model.add(Flatten()) # 쭉 늘여놓고
model.add(Dense(128, activation='relu'))
model.add(Dense(6, activation='softmax')) #마지막 Dense 6개 카테고리가 6개이니
model.summary()

model.compile(loss='categorical_crossentropy', optimizer='adam',
              metrics=['accuracy'])
fit_hist = model.fit(x_train, y_train, batch_size=128,
                     epochs=10, validation_data=(x_test, y_test))
score = model.evaluate(x_test, y_test, verbose=0)
print('Final test set accuracy', score[1])
model.save('./models/news_section_classification_model_{}.h5'.format(score[1]))
plt.plot(fit_hist.history['val_accuracy'], label='val accuracy')
plt.plot(fit_hist.history['accuracy'], label='accuracy')
plt.legend()
plt.show()