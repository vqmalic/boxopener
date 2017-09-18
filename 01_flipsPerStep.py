import pandas as pd
import numpy as np

df = pd.read_pickle("runs/2017_09_17_13_39_18_iter10000.pkl")

flips = []

for i in range(df.shape[0]-1):
	thisrow = df.iloc[i]
	nextrow = df.iloc[i+1]
	flips.append(sum(thisrow != nextrow))

flips = np.array(flips)

winsize = 101
win = np.convolve(flips, np.ones((winsize,)), mode="valid")

plt.plot(np.arange(np.ceil(winsize/2), len(win) + np.ceil(winsize/2)), win)
plt.title("Switches per Window, (window size = {})".format(winsize))
plt.xlabel("Time (t)")
plt.ylabel("Switches")
plt.savefig("figures/switches_per_step_ALL.png")


# By quadrant

q1_i = np.concatenate([np.arange(10) + (10 * i) for i in range(0, 20, 2)])
q2_i = np.concatenate([np.arange(10) + (10 * i) for i in range(1, 21, 2)])
q3_i = np.concatenate([np.arange(200, 210) + (10 * i) for i in range(0, 20, 2)])
q4_i = np.concatenate([np.arange(200, 210) + (10 * i) for i in range(1, 21, 2)])

plt.cla()

fig, axes = plt.subplots(2, 2)

quads = [q1_i, q2_i, q3_i, q4_i]
wins = []

for i, d in enumerate(quads):
	sub = df.iloc[:, d]
	flips = []
	for j in range(df.shape[0]-1):
		thisrow = sub.iloc[j]
		nextrow = sub.iloc[j+1]
		flips.append(sum(thisrow != nextrow))
	flips = np.array(flips)
	winsize = 501
	win = np.convolve(flips, np.ones((winsize,)), mode="valid")
	wins.append(win)

allmax = np.max([np.max(x) for x in wins])

for i, ax in enumerate(axes.flatten()):
	win = wins[i]
	xvals = np.arange(np.ceil(winsize/2), len(win) + np.ceil(winsize/2))
	ax.plot(xvals, win)
	ax.set_title("Quadrant {}".format(i+1))

plt.tight_layout()
fig.show()