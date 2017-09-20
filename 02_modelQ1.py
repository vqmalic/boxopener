import pandas as pd
import numpy as np
import os

df = pd.read_pickle("runs/2017_09_17_13_39_18_iter10000.pkl")
q1_i = np.concatenate([np.arange(10) + (10 * i) for i in range(0, 20, 2)])
q2_i = np.concatenate([np.arange(10) + (10 * i) for i in range(1, 21, 2)])
q3_i = np.concatenate([np.arange(200, 210) + (10 * i) for i in range(0, 20, 2)])
q4_i = np.concatenate([np.arange(200, 210) + (10 * i) for i in range(1, 21, 2)])

def makeDataPoint(q, t, target, padsize):
	# Gets neighbors that are within padsize of target (inclusive)
	# Also, next state of i to target
	x = q.iloc[t, target]
	thisrow = np.array(q.iloc[t, :])
	thismat = thisrow.reshape(10, 10)
	row = target // 10
	col = target - (10 * row)
	out = []
	for i in range(row-padsize, row+padsize+1):
		for j in range(col-padsize, col+padsize+1):
			if i < 0 or j < 0 or i >= 10 or j >= 10:
				out.append(-1)
			elif i == row and j == col:
				pass
			else:
				out.append(thismat[i, j])
	y = q.iloc[t+1, target]
	return((out, x, y))

data = []

for path in os.listdir("runs"):
	if "10000" in path:
		print(path)
		df = pd.read_pickle("runs/{}".format(path))
		q1 = df.iloc[:, q1_i]
		for row in range(q1.shape[0] - 1):
			for col in range(q1.shape[1]):
				data.append(makeDataPoint(q1, row, col, 1))

'''
neighborcount = []
for row in data:
	bcount = row[0].count(0)
	wcount = row[0].count(1)
	x = row[1]
	y = row[2]
	if x == y:
		state = "noswitch"
	elif x == 0:
		state = "towhite"
	else:
		state = "toblack"
	neighborcount.append((bcount, wcount, x, y, state))

import pandas as pd

df = pd.DataFrame(neighborcount, columns=['bcount', 'wcount', 'before', 'after', 'state'])
'''