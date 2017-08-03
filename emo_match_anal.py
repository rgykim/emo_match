#!/usr/bin/env python

### Emotional Go/No-Go Task Results Analysis Script
### Creator: Robert Kim
### Last Modifier: Robert Kim
### Version Date: 15 Jan 2017
### Python 2.7 

### Assumptions: 	blocks files = [EMO_Calm_Female.csv, EMO_Calm_Male.csv, EMO_Happy_Final.csv, EMO_Fearful_Final.csv]
### 				header fieldnames are constant across input files

import csv
import os
import sys
import time

### opens sys.stdout in unbuffered mode
### print (sys.stdout.write()) operation is automatically flushed after each instance
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

### set home directory
home_dir = os.path.dirname(os.path.abspath(__file__))
# home_dir = '/Volumes/projects_herting/NEAT/Visit_2/V2_Data'
os.chdir(home_dir)

blocks = ["FEMALE", "MALE", "HAPPY", "FEARFUL"]
block_dict = dict(zip(blocks, range(4)))

### this code is FUCKING BALLER
def analysis(in_file):
	with open(in_file, 'rb') as csvfile:
		reader = csv.DictReader(csvfile)
		header = reader.fieldnames
		raw_data = list(reader)

	raw_data[:] = [row for row in raw_data if row['stim']]

	total, acc, miss, falarm = [[0 for i in range(4)] for j in range(4)]
	rt = [[] for i in range(4)]

	for row in raw_data:
		total[block_index(row)] += 1

		if row['key_resp_2.corr'] == '1':
			acc[block_index(row)] += 1
			if row['key_resp_2.keys'] == 'space':
				rt[block_index(row)].append(float(row['key_resp_2.rt']))
		elif row['corrAns'] == 'space':
			miss[block_index(row)] += 1
		elif row['corrAns'] in ['None', 'nan']:
			falarm[block_index(row)] += 1

	if total != [15, 15, 30, 30]:
		print total
		raise ValueError("INVALID CONSTRUCTION OF TRIALS")

	acc[:] = [float(i)/float(j)*100 for i, j in zip(acc, total)]
	rt[:] = [[mean(x), stdev(x)] for x in rt]
	
	for i, s in enumerate(blocks):
		print "\t%s Block Statistics: " % s
		print "\t\tAccuracy = %.2f%%" % acc[i]
		print "\t\tResponse Time (Avg; Stdev) = %.4fs; %.4fs" % (rt[i][0], rt[i][1])
		print "\t\tMisses = %d" % miss[i]
		print "\t\tFalse Alarms = %d" % falarm[i]

	basename = os.path.basename(in_file)
	n = basename.index('.csv')
	out_dir = "GNG_analysis_results"
	out_file = os.path.join(out_dir, basename[ :n] + "_ANALYSIS.csv")
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	with open(out_file, 'wb') as out_csv:
		writer = csv.writer(out_csv, delimiter = ',', quotechar = '"')
		out_arr = [[""] + blocks[:]]
		for x, y in zip(["accuracy", "rt_avg", "rt_stdev", "miss", "f_alarm"], [acc, [x[0] for x in rt], [x[1] for x in rt], miss, falarm]):
			out_arr.append([x] + [y[i] for i in range(4)])

		writer.writerows(out_arr)	

def block_index(row):
	k = [k for (k, v) in block_dict.items() if "_" + k in row['Condition'].upper()]
	if len(k) != 1:
		raise ValueError("INVALID CONDITION CONSTRUCTION")
	return block_dict.get(k[0], ValueError("INVALID RANGE"))

def mean(arr):
	return float(sum(arr))/float(len(arr))

def run_analysis(arr):
	error_files = []
	for x in arr:
		try:
			print "\n::::: ANALYZING %s :::::" % x
			analysis(x)
		except ZeroDivisionError: 
			print ">> ERROR READING " + x
			print ">> ZERO DIVISION ERROR: CHECK FILE CONSTRUCTION"
			error_files.append(x)

	if error_files:
		print "\n>> TOTAL OF %d INVALID FILES" % len(error_files)
		print ">> LIST OF FILES THAT THREW EXCEPTION:\n>>",
		print '\n>>'.join(error_files)

def stdev(arr):
    mn = mean(arr)
    var = sum([(x-mn)**2 for x in arr])/len(arr)
    return var**0.5

### MAIN ###

print "Script file directory: %s" % home_dir
print "Subdirectories found in script file directory:\n"

for x in list(enumerate(next(os.walk(home_dir))[1])):
	print "    ", 
	print x
print ""

dir_input = raw_input("Please enter the desired working subdirectory: ")

try:
	dir_index = int(dir_input)
except ValueError:
	sys.exit(	"EXITING OPERATION\n" + 
				"No subdirectory was properly selected"		)

sub_dir = next(os.walk(home_dir))[1][dir_index]
print "\nNew working directory: %s" % os.path.join(home_dir, sub_dir)

csv_list = []

for root, dirs, files in os.walk(sub_dir):
    for f in files:
        if f.endswith(".csv"):
             csv_list.append(os.path.join(root, f))

if not csv_list:
	sys.exit(	"EXITING OPERATION\n" + 
				"No CSV files were found in working directory.\n" + 
				"Please place the script file into the proper directory and try again."	)

print "\nCSV files found in working directory:\n"

for x in list(enumerate(csv_list)):
	print "    ", 
	print (x[0], "/".join(x[1].strip("/").split('/')[1:]))
print ""

csv_input = raw_input("Please enter the desired CSV file index (or multiple indices separated by spaces): ")

if not csv_input:
	sys.exit(	"EXITING OPERATION\n" + 
				"No CSV files were properly selected"	)

csv_index = csv_input.split()
csv_index = [int(a) for a in csv_index]

if not all(n in range(len(csv_list)) for n in csv_index):
	sys.exit(	"EXITING OPERATION\n" +
				"INVALID ENTRY OF FILE INDICES"	)

input_list = [csv_list[n] for n in csv_index]
run_analysis(input_list)

print "\nOPERATION COMPLETED " + time.strftime("%d %b %Y %H:%M:%S", time.localtime())