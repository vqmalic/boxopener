import requests
import re
import pandas as pd
from clint.textui import progress
from bs4 import BeautifulSoup
from datetime import datetime

# Class labels of matrix cells seem to indicate that each color represents an airport
airportdict = {
	"bru": "Brussels",
	"gru": "Sao Paulo",
	"hkg": "Hong Kong",
	"icn": "Incheon",
	"jfk": "New York",
	"las": "Las Vegas",
	"lax": "Los Angeles",
	"lis": "Lisbon",
	"mex": "Mexico City",
	"pty": "Panama City"
}

colordict = {
	"bru": (255, 0, 0),
	"gru": (0, 0, 0),
	"hkg": (255, 165, 0),
	"icn": (255, 192, 203),
	"jfk": (0, 0, 255),
	"las": (0, 255, 255),
	"lax": (255, 0, 255),
	"lis": (0, 128, 0),
	"mex": (255, 255, 255),
	"pty": (128, 128, 128)
}

# Let's assign numbers as IDs to colors for better numpy arrays

iddict = {
	"mex": 1,
	"gru": 0,
	"bru": 2,
	"hkg": 3,
	"icn": 4,
	"jfk": 5,
	"las": 6,
	"lax": 7,
	"lis": 8,
	"pty": 9
}


def extract(result):
	c = result.content
	soup = BeautifulSoup(c, "lxml")

	# Get step number
	ctext = soup.body.findAll(text=re.compile("Current"))[0]
	step = int(ctext.split()[-1])

	# Get colors
	grid = []

	rows = soup.findAll("tr")
	for row in rows:
		cells = row.findAll("td")
		for cell in cells:
			label = cell['class'][0]
			grid.append(label)
	grid = [iddict[x] for x in grid]
	return(step, grid)

cycles = 1
iterations = 1000
starturl = "http://homes.soic.indiana.edu/rocha/academics/i501/blackbox/BlackBox.php?reset=1&cycles_input={}"
nexturl = "http://homes.soic.indiana.edu/rocha/academics/i501/blackbox/BlackBox.php?cycles={}"

seq = []

# Get initial
s = requests.session()
result = s.get(starturl.format(cycles))
step, grid = extract(result)
seq.append((step, grid))

# Iterate

starttime = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

with progress.Bar(expected_size=iterations) as bar:
	for i in range(iterations):
		result = s.get(nexturl.format(cycles))
		step, grid = extract(result)
		seq.append((step, grid))
		bar.show(i)

indices = [x[0] for x in seq]
grids = [x[1] for x in seq]

df = pd.DataFrame(grids, index=indices)

df.to_pickle("runs/{}_iter{}.pkl".format(starttime, iterations))