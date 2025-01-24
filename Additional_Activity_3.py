import pandas as pd 

a = [1, 5, 5, 6, 2, 8, 8, 5, 2, 6, 9, 7, 4, 3, 7, 2]

cleaned_data = pd.DataFrame(a)

print("dataset: ", cleaned_data)
print("duplicated data seperated with boolean values: \n", cleaned_data.duplicated())