#!/usr/bin/python

import sys, sqlite3, os, time
import numpy as np

from operator import itemgetter

class test:

	### Initialize ###

	# Read in sentences from test.db
	conn = sqlite3.connect('../data/test.db')
	print "Successful connection to training database"
	c = conn.cursor()
	c.execute("SELECT * FROM sentences")
	results = c.fetchall()
	conn.commit()
	conn.close()

	# Open file of word percentages
	with open("republicanPercent.txt", "r+") as pr:
		pRepFile = pr.readlines()
	with open("democratPercent.txt", "r+") as pd:
		pDemFile = pd.readlines()

	# Variables
	rScore = 0.0
	dScore = 0.0
	correct = 0
	wrong = 0
	demWords = [[],[]]
	repWords = [[],[]]
	repArray = []
	demArray = []

	# Get most Democratic and Republican Words
	for line in pDemFile:
		line = line.split('\t')
		freq = line[1].split('\n')
		demWords.append([[float(freq[0])],[line[0]]])
	demWords.sort(reverse=True)

	for line in pRepFile:
		line = line.split('\t')
		freq = line[1].split('\n')
		repWords.append([[float(freq[0])],[line[0]]])
	repWords.sort(reverse=True)

	m = 0
	while m < 100:
		d = demWords[m]
		r = repWords[m]
		demArray.append(str(m) + " " + d[1][0])
		repArray.append(str(m) + " " + r[1][0])
		m+=1

	new = list(set(demArray) & set(repArray))
	#print float(len(new))/25.0
	print demArray
	print repArray

	# Calculate Accuracy
	#for row in results:
	#	partyActual = row[0]
	#	sentence = row[1].split()
	#	for word in sentence:
	#		i = 0
	#		while i < len(demWords) - 2:
	#			check = demWords[i][1]
	#			val = demWords[i][0]
	#			if check[0] == word:
	#				dScore += val[0]
	#			i += 1
	#		i = 0
	#		while i < len(repWords) - 2:
	#			check = repWords[i][1]
	#			val = repWords[i][0]
	#			if check[0] == word:
	#				rScore += val[0]
	#			i += 1
	#	if dScore > rScore:
	#		if partyActual == "Democratic":
	#			correct += 1
	#		else:
	#			wrong += 1
	#	else:
	#		if partyActual == "Republican":
	#			correct += 1
	#		else:
	#			wrong += 1
	#	accuracy = float(correct) / float(correct + wrong)
	#	print "Accuracy: ",accuracy

	print "Time: ",time.clock()

