####################################################
# This script splits the sentences into 80%        #
# training data and 20% test data with each of     #
# these datasets containing 50% Republican         #
# sentences and 50% Democratic sentences.          #
####################################################

# TODO: WORK IN PROGRESS

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
        os.remove(training_database_filename)
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

# Separate out the parties and speeches
# (noting that the speeches[i] speech was said by the parties[i] party)
parties = []
speeches = []
for result in all_results:
    parties.append(result[1])
    speeches.append(result[3])

# Save the sentences for each party
democratic_sentences = []
republican_sentences = []

for i in range(len(speeches)):

    sentences = speeches[i].split('. ')

    if parties[i] == "Democratic":
        for sentence in sentences:
            democratic_sentences.append(sentence)

    elif parties[i] == "Republican":
        for sentence in sentences:
            republican_sentences.append(sentence)

    else:
        print("ERROR! Invalid party {0}".format(parties[i]))

# Create the sentences SQL file
conn = sqlite3.connect(sentence_database_filename)
c = conn.cursor()
c.execute('''CREATE TABLE sentences (party text, sentence text)''')

# Populate the sentences SQL file
for sentence in democratic_sentences:
    c.execute("INSERT INTO sentences VALUES (?, ?)", ("Democratic", sentence))

for sentence in republican_sentences:
    c.execute("INSERT INTO sentences VALUES (?, ?)", ("Republican", sentence))

conn.commit()
conn.close()
