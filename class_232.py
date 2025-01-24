from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense

dataset = loadtxt('diabetes_dataset.csv', delimiter=',')

x = dataset[:,0:8]
y = dataset[:,8]

model = Sequential()

model.add(Dense(12, input_dim=8, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.summary()
model.compile(loss="binary_crossentropy", metrics=['accuracy'])

model.fit(x, y, epochs=1000, batch_size=200)

predictions = model.predict(x)

for i in range(5):
	print(f'{x[i].tolist()} => {predictions[i]} expected {y[i]}')