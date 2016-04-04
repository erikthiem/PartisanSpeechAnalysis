####################################################
# This script splits the sentences into 80%        #
# training data and 20% test data with each of     #
# these datasets containing 50% Republican         #
# sentences and 50% Democratic sentences.          #
####################################################

import random

class Sentence():
    
    def __init__(self, party, text):
        self.party = party
        self.text = text


import sqlite3
import os.path

sentence_database_filename = "sentences.db"
training_database_filename = "train.db"
testing_database_filename = "test.db"

# Error checking for sentence database file existence
if not os.path.isfile(sentence_database_filename):
    print("\nError. '{0}' file not found. Exiting.\n".format(sentence_database_filename))
    exit(-1)

# Error checking for training database file existence
if os.path.isfile(training_database_filename) or os.path.isfile(testing_database_filename):
    answer = raw_input("Database '{0}' or '{1}' already exist.\nAre you sure you want to delete and re-create them? (y/n): ".format(training_database_filename, testing_database_filename)).lower()
    if (answer == 'y' or answer == 'yes'):
        print("Re-creating databases.\n")

        if os.path.isfile(training_database_filename):
            os.remove(training_database_filename)
        if os.path.isfile(testing_database_filename):
            os.remove(testing_database_filename)

    else:
        print("Exiting.\n")
        exit(-1)

# Access the sentences SQL file
conn = sqlite3.connect(sentence_database_filename)
c = conn.cursor()
c.execute('SELECT * FROM sentences;')
all_results = c.fetchall()
conn.commit()
conn.close()

# Save the results to objects
democratic_sentences = []
republican_sentences = []

for result in all_results:
    s = Sentence(result[0], result[1])
    if s.party == "Republican":
        republican_sentences.append(s)
    else:
        democratic_sentences.append(s)

print len(republican_sentences)
print len(democratic_sentences)

# Randomly lob off the bigger of the datasets (Democratic in this case) so that 
# they are the same size. This is important, especially for Naive Bayes.
random.shuffle(democratic_sentences)
democratic_sentences = democratic_sentences[0:len(republican_sentences)]

# Now that these are the same size, split these into training and test
random.shuffle(democratic_sentences)
random.shuffle(republican_sentences)
split_index = int(len(democratic_sentences) * 0.80)

training_democratic_sentences = democratic_sentences[:split_index]
training_republican_sentences = republican_sentences[:split_index]

testing_democratic_sentences = democratic_sentences[split_index:]
testing_republican_sentences = republican_sentences[split_index:]

training_sentences = training_democratic_sentences + training_republican_sentences
test_sentences = testing_democratic_sentences + testing_republican_sentences

# One last shuffle to mix the democrats and republicans
random.shuffle(training_sentences)
random.shuffle(test_sentences)

# Create the training sentences SQL file
conn = sqlite3.connect(training_database_filename)
c = conn.cursor()
c.execute('''CREATE TABLE sentences (party text, sentence text)''')

# Populate the training sentences SQL file
for sentence in training_sentences:
    c.execute("INSERT INTO sentences VALUES (?, ?)", (sentence.party, sentence.text))

conn.commit()
conn.close()

# Create the test sentences SQL file
conn = sqlite3.connect(testing_database_filename)
c = conn.cursor()
c.execute('''CREATE TABLE sentences (party text, sentence text)''')

# Populate the test sentences SQL file
for sentence in test_sentences:
    c.execute("INSERT INTO sentences VALUES (?, ?)", (sentence.party, sentence.text))

conn.commit()
conn.close()
