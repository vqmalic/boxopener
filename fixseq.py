import os
import pandas as pd

colordict = {
	"bru": (255, 0, 0), #red
	"gru": (0, 0, 0), # black
	"hkg": (255, 165, 0), # orange
	"icn": (255, 192, 203), # pink
	"jfk": (0, 0, 255), # blue
	"las": (0, 255, 255), # aqua
	"lax": (255, 0, 255), # magenta
	"lis": (0, 128, 0), # green
	"mex": (255, 255, 255), # white
	"pty": (128, 128, 128) # gray
}

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

remap = {
	1 : 9, # mex, white, 1 to 9
	0 : 0, # gru, black, 0 to 0
	2 : 6, # bru, red, 2 to 6
	3 : 7, # hkg, orange, 3 to 7
	4 : 8, # icn, pink, 4 to 8
	5 : 2, # jfk, blue, 5 to 2
	6 : 4, # las, aqua, 6 to 4
	7 : 3, # lax, magenta, 7 to 3
	8 : 5, # lis, green, 8 to 5
	9 : 1  # pty, gray, 9 to 1
}

for path in os.listdir("runs"):
	print(path)
	df = pd.read_pickle("runs/{}".format(path))
	for i in df.columns:
		df.loc[:, i] = df.loc[:, i].map(remap)
	df.to_pickle("runs/{}".format(path))
