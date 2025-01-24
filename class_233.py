import pandas as pd

data = pd.read_csv("radar_data.csv")

data.loc[data["distance"] <= 17, "action"] = "1"
data.loc[data["steer"] < 0, "action"] = "0"
data.loc[data["distance"] > 17, "action"] = "2"

data.to_csv('new_radarandistance.csv', index=False)
print(data)