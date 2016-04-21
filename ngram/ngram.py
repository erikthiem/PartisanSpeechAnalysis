import collections
import nltk
import os
import random
import sqlite3
import sys
import time

from collections import Counter
from random import choice

class Sentence():
    
    def __init__(self, text):
        self.text = "STARTSTARTSTART " + text + "FINISHFINISHFINISH"


def sentencesFromDB(db_file_path, party):

    conn = sqlite3.connect(db_file_path)
    c = conn.cursor()
    if party == 'Republican':
    	c.execute('SELECT sentence FROM sentences WHERE party ="Republican";')
    else:
    	c.execute('SELECT sentence FROM sentences WHERE party ="Democratic";')
    results = c.fetchall()
    conn.commit()
    conn.close() 

    sentences = [] 
    for r in results:
        s = Sentence(r[0])
        sentences.append(s)

    return sentences

def bigram(text):

	bigrams = []
	biCounts = Counter()

	for sentence in text:

		# tokenize the words in the sentence
		tokens = nltk.word_tokenize(sentence.text)

		if len(tokens) >= 2:
			location = 0
			for token in tokens[:len(tokens) - 1]:
				bigrams.append((token, tokens[location + 1]))
				location += 1

	for gram in bigrams:
		biCounts[gram] += 1

	return biCounts.most_common()


def trigram(text):

	trigrams = []
	triCounts = Counter()

	for sentence in text:

		# tokenize the words in the sentence
		tokens = nltk.word_tokenize(sentence.text)

		if len(tokens) >= 3:
			location = 0
			for token in tokens[:len(tokens) - 2]:
				trigrams.append((token, tokens[location + 1], tokens[location + 2]))
				location += 1

	for gram in trigrams:
		triCounts[gram] += 1

	return triCounts.most_common()

def weighted_choice(choices):
	total = sum(w for c, w in choices)
	r = random.uniform(0, total)
	upto = 0
	for c, w in choices:
		if upto + w >= r:
			return c
		upto += w
	assert False, "Reached end of weighted_choice, this shouldnt happen!"

def generateSentencesFromBigrams(bigramList, numberOfSentences):
	# Store une-bigram pairs in a list of tuples
	# Each tuple has a unigram, then a list of tuples
	# Each tuple has a bigram that begins with the unigram, and the count

	# # # # # # # # # # # # # # # # # # # # # # # #
	# THIS IS THE MASTER LIST OF WORD-GRAM PAIRS  #
	# # # # # # # # # # # # # # # # # # # # # # # #
	ubPairs = []
	
	counter = 0

	while counter < numberOfSentences:

		# Begin with <s>
		currentWord = "STARTSTARTSTART"
		currentBiList = []

		# First, get list of all the words that follow the currentWord
		for gram, amount in bigramList:
			if gram[0] == currentWord:
				currentBiList.append((gram, amount))

		ubPairs.append((currentWord, currentBiList))
		nextGram = weighted_choice(currentBiList)
		currentSentence = nextGram[1]
		currentWord = nextGram[1]

		while "FINISHFINISHFINISH" not in currentWord:

			wordInUBPairs = False
			currentBiList = []

			for gram, biList in ubPairs:
				if currentWord == gram:
					currentBiList = biList
					wordInUBPairs = True
					break

			if wordInUBPairs == False:
				# create new bigram list for this unigram
				for gram, amount in bigramList:
					if gram[0] == currentWord:
						currentBiList.append((gram, amount))
				# add to ubPairs
				ubPairs.append((currentWord, currentBiList))
			
			nextGram = weighted_choice(currentBiList)
			if "FINISHFINISHFINISH" in nextGram[1]:
				currentSentence = currentSentence + "."
			else:
				currentSentence = currentSentence + " " + nextGram[1]
			currentWord = nextGram[1]

		print("({0}) {1}".format(counter + 1, currentSentence))
		counter += 1

	print("\n")

def generateSentencesFromTrigrams(trigramList, bigramList, numberOfSentences):

	btPairs = []
	counter = 0

	while counter < numberOfSentences:

		currentWord = "STARTSTARTSTART"
		currentBiList = []

		for gram, amount in bigramList:
			if gram[0] == currentWord:
				currentBiList.append((gram, amount))
		nextGram = weighted_choice(currentBiList)
		currentSentence = nextGram[1]
		
		currentBigram = ("STARTSTARTSTART", nextGram[1])
		currentTriList = []

		for gram, amount in trigramList:
			if (gram[0], gram[1]) == currentBigram:
				currentTriList.append((gram, amount))

		btPairs.append((currentBigram, currentTriList))
		nextGram = weighted_choice(currentTriList)
		currentSentence = currentSentence + " " + nextGram[2]
		currentBigram = (nextGram[1], nextGram[2])

		while "FINISHFINISHFINISH" not in currentBigram[1]:

			wordInBTPairs = False
			currentTriList = []

			for gram, triList in btPairs:
				if currentBigram == gram:
					currentTriList = triList
					wordInBTPairs = True
					break

			if wordInBTPairs == False:
				for gram, amount in trigramList:
					if (gram[0], gram[1]) == currentBigram:
						currentTriList.append((gram, amount))
				btPairs.append((currentBigram, currentTriList))

			nextGram = weighted_choice(currentTriList)
			currentSentence = currentSentence + " " + nextGram[2]
			currentBigram = (nextGram[1], nextGram[2])

		print("({0}) {1}".format(counter + 1, currentSentence))
		counter += 1

	print("\n")

if __name__ == "__main__":

	if len(sys.argv) != 2:
		print("\nError! Expected syntax: 'python ngram.py data_path ")

	data_path = sys.argv[1]

	if not os.path.isfile(data_path):
		print("Error! database {0} does not exist.\n")
		exit(-1)

	# Load the data
	print("Creating Republican sentences")
	sentences_R = sentencesFromDB(data_path, 'Republican')
	print("Creating Democratic sentences\n")
	sentences_D = sentencesFromDB(data_path, 'Democratic')

	# Create bigram lists
	print("Creating Republican bigrams")
	bigrams_R = bigram(sentences_R)
	print("Creating Democratic bigrams")
	bigrams_D = bigram(sentences_D)

	# Create trigram lists
	print("Creating Republican trigrams")
	trigrams_R = trigram(sentences_R)
	print("Creating Democratic trigrams")
	trigrams_D = trigram(sentences_D)

	print("\n~*~*~*~*~*~*~*\nGrams Created!\n~*~*~*~*~*~*~*\n");

	print("Generate Republican sentences from Bigrams")
	generateSentencesFromBigrams(bigrams_R, 10)
	print("Generate Democratic sentences from Bigrams")
	generateSentencesFromBigrams(bigrams_D, 10)
	print("\n")

	print("Generate Republican sentences from Trigrams")
	generateSentencesFromTrigrams(trigrams_R, bigrams_R, 10)
	print("Generate Democratic sentences from Trigrams")
	generateSentencesFromTrigrams(trigrams_D, bigrams_D, 10)