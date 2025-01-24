import pandas as pd

dataframe = pd.read_csv("expenses.csv")

sum_data = dataframe.sum()
print("total sum of expenses with sum function: \n", sum_data)