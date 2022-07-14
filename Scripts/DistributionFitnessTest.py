import numpy as np
from scipy import stats as st
import sys
import csv
from distfit import distfit

def plot_data(file_name, i):
	data = []

	with open(file_name, 'r') as f:
		lines = csv.reader(f, delimiter=",")
		for row in lines:
			data.append(round(float(row[i]), 3))

	data = np.array(data).astype("float")

	dist = distfit()

	dist.fit_transform(data)

	print(dist.summary)

if __name__ == "__main__":
	plot_data(sys.argv[1], int(sys.argv[2])) #filename + csv file column
