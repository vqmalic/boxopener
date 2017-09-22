import pandas as pd
import numpy as np
import os

import matplotlib.pyplot as plt

from collections import Counter


def entropy(x):
	counts = Counter(x)
	total = len(x)
	probs = np.array([c/total for c in counts.values()])
	return -np.sum(probs * np.log2(probs))


paths = os.listdir("runs")
runs = [pd.read_pickle("runs/{}".format(path)) for path in paths]

entropies = []

for t in range(runs[0].shape[0]):
	grid = []
	for i in range(runs[0].shape[1]):
		vals = [x.iloc[t, i] for x in runs]
		e = entropy(vals)
		grid.append(e)
	entropies.append(grid)

for df in runs:
	plt.imshow(df.iloc[-1, :].reshape(20, 20))
	plt.show()

