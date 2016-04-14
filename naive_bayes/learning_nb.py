#!/usr/bin/python

import sys

### Initialization ###

# Open text files
repFile = file.open("republicanWords.txt","r+")
demFile = file.open("democratWords.txt","r+")

### Learning ###
class learn:

	## Republican ##
	# Calculate number of terms
	for line in repFile:
		line = line.split("\t")
		repTotal = repTotal + int(line[1])
	
		# 


	## Democrat ##
	# Calculate number of terms
	for line in demFile:
		line = line.split("\t")
		demTotal = demTotal + int(line[1])

		# 
	

#class test:

	# Read in speech

	
	# Assign each word a party [& politician]


	# Estimate speech's party [& politician]
