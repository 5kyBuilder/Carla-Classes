import pandas as pd 

a = {"Products" : [1, 7, 2]}
b = {"Calories" : [420, 380, 390]}

dataframeA = pd.DataFrame(a)
dataframeB = pd.DataFrame(b)

combinedDataframe = pd.concat([dataframeA, dataframeB], axis=1, join="inner")

print("concatenated dataframes in one: \n", combinedDataframe)