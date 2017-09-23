import requests
import re
import pandas as pd
from clint.textui import progress
from bs4 import BeautifulSoup
from datetime import datetime

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

no = 10000

starts = []
s = requests.session()

with progress.Bar(expected_size=no) as bar:
	for i in range(no):
		result = s.get("http://homes.soic.indiana.edu/rocha/academics/i501/blackbox/BlackBox.php?reset=1&cycles_input=0")
		step, grid = extract(result)
		starts.append(grid)
		bar.show(i)

df = pd.DataFrame(starts)
starttime = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
df.to_pickle("starts/{}_{}starts.pkl".format(starttime, no))