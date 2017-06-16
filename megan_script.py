#!/usr/bin/env python

### Hack to do stuff for Megan
### 30 May 2017

import csv
import os
import sys
import time

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
home_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(home_dir)

def main():
	subject_input = raw_input("subject_runNum: ")

	csv_list = []
	for root, dirs, files in os.walk(home_dir):
		for f in files:
			if subject_input in f:
				csv_list.append(os.path.join(root, f))

	print '\n'.join(csv_list)
	if len(csv_list) < 2:
		sys.exit("Something went terribly wrong and you should feel ashamed about it.")

	with open(subject_input + '_averaged_results.csv', 'rb') as csvfile:
		reader = csv.DictReader(csvfile)
		header = reader.fieldnames
		avg_data = list(reader)

	emotional, neutral, shapes = [[] for n in range(3)]
	for row in avg_data:
		if 'EmoFaceBlock' in row['Block_Name']:
			emotional.append([row['Block_Start_Time'], 18, 1])
		elif 'NeuFaceBlock' in row['Block_Name']:
			neutral.append([row['Block_Start_Time'], 18, 1])
		elif 'ShapeBlock' in row['Block_Name']:
			shapes.append([row['Block_Start_Time'], 18, 1])

	with open(subject_input + '_results.csv', 'rb') as csvfile:
		reader = csv.DictReader(csvfile)
		header = reader.fieldnames
		raw_data = list(reader)

	fixation = [[float(row['Time_of_trial']) + 2, 11, 1] for row in raw_data[5: :6]]

	with open(subject_input + '_emotional_faces.txt', 'wb') as out_csv:
		writer = csv.writer(out_csv, delimiter = '\t', quotechar = '"')
		writer.writerows(emotional)

	with open(subject_input + '_neutral_faces.txt', 'wb') as out_csv:
		writer = csv.writer(out_csv, delimiter = '\t', quotechar = '"')
		writer.writerows(neutral)

	with open(subject_input + '_shapes.txt', 'wb') as out_csv:
		writer = csv.writer(out_csv, delimiter = '\t', quotechar = '"')
		writer.writerows(shapes)

	with open(subject_input + '_fixation.txt', 'wb') as out_csv:
		writer = csv.writer(out_csv, delimiter = '\t', quotechar = '"')
		writer.writerows(fixation)

if __name__ == '__main__':	
	main()