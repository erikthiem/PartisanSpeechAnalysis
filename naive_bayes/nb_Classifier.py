#!/usr/bin/python

import sys, sqlite3, re, string

class train:
	
	### Initialize ###
	# Takes 12.5 minutes to run, consider moving the word & count array creation to a new file
	
	# Lists of words used in Republican and Democrat speeches
	repWords = []
	repCounts = []
	demWords = []
	demCounts = []
	totWords = []
	totCounts = []

	# Create files to store republican and democratic words
	fr = open("republicanWords.txt", "rw+")
	fd = open("democratWords.txt", "rw+")
	f = open("words.txt", "rw+")

	# Read in sentences from train.db
	conn = sqlite3.connect('../data/train.db')
	print "Successful connection to training database"
	dbCursor = conn.execute("SELECT * FROM sentences")

	# Get sentence's party [& politician] classification
	for row in dbCursor:
		print "Damn this thing is huge" + row[0]
		party = row[0]
		sentence = row[1].split()

		# Count number of times word is used in Republican speeches
		if party == "Republican":
			for word in sentence:
				
				# If word is jank, skip it
				if word.find('[^a-zA-Z0-9\']') < 0:
					
					# If word hasn't appeared yet, add it to list
					if repWords.count(word) == 0:
						repWords.append(word)
						repCounts.append(1)
					
					# Otherwise increment its count by 1
					else:
						repCounts[repWords.index(word)] += 1

		# Count number of times word is used in Democrat speeches
		else:
			for word in sentence:

				# If word is jank, skip it
				if word.find('[^a-zA-Z0-9\']') < 0:
				
					# If word hasn't appeared yet, add it to list
					if demWords.count(word) == 0:
						demWords.append(word)
						demCounts.append(1)
					
					# Otherwise increment its count by 1
					else:
						demCounts[demWords.index(word)] += 1

		# Count number of times word is used
		for word in sentence:
				
				# If word is jank, skip it
				if word.find('[^a-zA-Z0-9\']') < 0:
					
					# If word hasn't appeared yet, add it to list
					if totWords.count(word) == 0:
						totWords.append(word)
						totCounts.append(1)
					
					# Otherwise increment its count by 1
					else:
						totCounts[totWords.index(word)] += 1

	# Write word & count pairs to file
	for index in range(len(repWords)):
		fr.write(repWords[index] + "\t" + str(repCounts[index]) + "\n")

	for index in range(len(demWords)):
		fd.write(demWords[index] + "\t" + str(demCounts[index]) + "\n")

	for index in range(len(totWords)):
		f.write(totWords[index] + "\t" + str(totCounts[index]) + "\n")
	
	fr.close()
	fd.close()
	f.close()

	# Close connection to train.db
	print "We out fam"
	conn.close()
