import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from collections import defaultdict
df = pd.read_pickle("runs/2017_09_19_13_50_45_iter50000.pkl")

flips = []

for i in range(df.shape[0]-1):
	thisrow = df.iloc[i]
	nextrow = df.iloc[i+1]
	flips.append(sum(thisrow != nextrow))

flips = np.array(flips)

cflips = np.cumsum(flips)

plt.plot(cflips)
plt.show()

'''
winsize = 101
win = np.convolve(flips, np.ones((winsize,)), mode="valid")


plt.cla()
plt.plot(np.arange(np.ceil(winsize/2), len(win) + np.ceil(winsize/2)), win)
plt.title("Switches per Window, (window size = {})".format(winsize))
plt.xlabel("Time (t)")
plt.ylabel("Switches")
plt.savefig("figures/switches_ALL.png")
'''

# By quadrant

q1_i = np.concatenate([np.arange(10) + (10 * i) for i in range(0, 20, 2)])
q2_i = np.concatenate([np.arange(10) + (10 * i) for i in range(1, 21, 2)])
q3_i = np.concatenate([np.arange(200, 210) + (10 * i) for i in range(0, 20, 2)])
q4_i = np.concatenate([np.arange(200, 210) + (10 * i) for i in range(1, 21, 2)])

quads = [q1_i, q2_i, q3_i, q4_i]
qflips = {}

for i, d in enumerate(quads):
	sub = df.iloc[:, d]
	flips = []
	for j in range(df.shape[0]-1):
		thisrow = sub.iloc[j]
		nextrow = sub.iloc[j+1]
		flips.append(sum(thisrow != nextrow))
	flips = np.array(flips)
	qflips[i] = flips

fig, axes = plt.subplots(2, 2)

for i, ax in enumerate(axes.flatten()):
	flips = qflips[i]
	cflips = np.cumsum(flips)
	ax.plot(cflips)
	ax.set_title("Quadrant {}".format(i+1))

plt.tight_layout()
fig.savefig("cumulativeswitches_quadrant.png")

# do the same thing, but average it across all runs

paths = os.listdir("runs")
runs = [pd.read_pickle("runs/{}".format(path)) for path in paths]

qflips = defaultdict(list)

for counter, df in enumerate(runs):
	print(counter)
	for i, d in enumerate(quads):
		sub = df.iloc[:, d]
		flips = []
		for j in range(df.shape[0]-1):
			thisrow = sub.iloc[j]
			nextrow = sub.iloc[j+1]
			flips.append(sum(thisrow != nextrow))
		flips = np.array(flips)
		qflips[i].append(np.cumsum(flips))
