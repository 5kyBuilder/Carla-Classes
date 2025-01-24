import pandas as pd

dataset = pd.read_csv("expenses.csv")

print("data at 1st index are: \n", dataset.loc[1])