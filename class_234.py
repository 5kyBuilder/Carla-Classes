import pandas as pd 
from sklearn.neural_network import MLPClassifier

dataset = pd.read_csv('new_radar_distance_data.csv')

x = dataset.iloc[:, [2, 4]].values
y = dataset.iloc[:, 5].values

model = MLPClassifier(hidden_layer_sizes=(40),
						random_state=5,
						activation="relu",
						batch_size=500,
						learning_rate_init=0.1
	)

model.fit(x, y)

predictions = model.predict(x)
print("Predicted data: ", predictions)