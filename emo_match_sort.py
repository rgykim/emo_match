#!/usr/bin/python2.7

### Hack to do stuff for Megan

import csv
import os
import sys
import time

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
home_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(home_dir)

def main():
	subject_input = raw_input("subject ID: ")
	format_input = input("output format (1 = txt; 2 = csv): ")

	if format_input == 1:
		format = '.txt'
		delim = '\t'
	elif format_input == 2:
		format = '.csv'
		delim = ','
	else:
		sys.exit("Invalid file output format entered.")

	csv_list = []
	for root, dirs, files in os.walk(home_dir):
		for f in files:
			if subject_input.lower() in f.lower() and f.lower().endswith('_averaged_results.csv'):
				csv_list.append([root, f])

	f_index = 0
	if len(csv_list) < 1:
		sys.exit("No emo_match task files for provided subject ID.")
	elif len(csv_list) > 1:
		print "Search results: "
		for x in list(enumerate(csv_list)):
			print "    ", 
			print ("%d : " % x[0]) + os.path.join(x[1][0], x[1][1])
		print ""

		f_index = raw_input("Please enter the desired CSV file index (only select 1): ")
		try:
			f_index = int(f_index)
		except ValueError:
			sys.exit(	"EXITING OPERATION\n" + 
						"No file was properly selected"		)

	f_input = os.path.join(csv_list[f_index][0], csv_list[f_index][1][ :-len('_averaged_results.csv')])

	with open(f_input + '_averaged_results.csv', 'rb') as csvfile:
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

	with open(f_input + '_results.csv', 'rb') as csvfile:
		reader = csv.DictReader(csvfile)
		header = reader.fieldnames
		raw_data = list(reader)

	fixation = [[float(row['Time_of_trial']) + 2, 11, 1] for row in raw_data[5: :6]]

	with open(f_input[ :-2] + '_Emotional_faces' + format, 'wb') as out_csv:
		writer = csv.writer(out_csv, delimiter = delim, quotechar = '"')
		writer.writerows(emotional)

	with open(f_input[ :-2] + '_Neutral_faces' + format, 'wb') as out_csv:
		writer = csv.writer(out_csv, delimiter = delim, quotechar = '"')
		writer.writerows(neutral)

	with open(f_input[ :-2] + '_Shapes' + format, 'wb') as out_csv:
		writer = csv.writer(out_csv, delimiter = delim, quotechar = '"')
		writer.writerows(shapes)

	with open(f_input[ :-2] + '_Fixation' + format, 'wb') as out_csv:
		writer = csv.writer(out_csv, delimiter = delim, quotechar = '"')
		writer.writerows(fixation)

if __name__ == '__main__':	
	main()