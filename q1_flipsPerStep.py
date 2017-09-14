import pandas as pd

df = pd.read_pickle("runs/2017_09_14_17_39_48_iter1000.pkl")

flips = []

for i in range(df.shape[0]-1):
	thisrow = df.iloc[i]
	nextrow = df.iloc[i+1]
	flips.append(sum(thisrow != nextrow))