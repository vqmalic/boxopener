import pandas as pd
import numpy as np

df = pd.read_pickle("runs/2017_09_15_13_32_15_iter10000.pkl")

flips = []

for i in range(df.shape[0]-1):
	thisrow = df.iloc[i]
	nextrow = df.iloc[i+1]
	flips.append(sum(thisrow != nextrow))

flips = np.array(flips)
