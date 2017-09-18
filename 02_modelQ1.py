import pandas as pd
import numpy as np

df = pd.read_pickle("runs/2017_09_17_13_39_18_iter10000.pkl")
q1_i = np.concatenate([np.arange(10) + (10 * i) for i in range(0, 20, 2)])
q2_i = np.concatenate([np.arange(10) + (10 * i) for i in range(1, 21, 2)])
q3_i = np.concatenate([np.arange(200, 210) + (10 * i) for i in range(0, 20, 2)])
q4_i = np.concatenate([np.arange(200, 210) + (10 * i) for i in range(1, 21, 2)])

q1 = df.loc[:, q1_i]

def makeDataPoint(t, target, padsize):
	# Gets neighbors that are within padsize of target (inclusive)
	# Also, next state of i to target
	x = q1.iloc[t, target]
	thisrow = np.array(q1.iloc[t, :])
	thismat = thisrow.reshape(10, 10)
	row = target // 10
	col = target - (10 * row)
	out = []
	for i in range(row-padsize, row+padsize+1):
		for j in range(col-padsize, col+padsize+1):
			if i < 0 or j < 0 or i >= 10 or j >= 10:
				out.append(-1)
			else:
				out.append(thismat[i, j])
	y = q1.iloc[t+1, target]
	return((out, x, y))

data = []
for row in range(q1.shape[0] - 1):
	for col in range(q1.shape[1]):
		data.append(makeDataPoint(row, col, 1))