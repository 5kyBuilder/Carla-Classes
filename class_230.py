from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense
# load the dataset
dataset = loadtxt('diabetes_dataset.csv', delimiter=',')
# split into input (X) and output (y) variables
x = dataset[:,0:8]
y = dataset[:,8]
print('value of X are:', x)
print('value of Y are:', y)