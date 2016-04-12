####################################################
# This script parses the candidate speeches        #
# database to generate sentences that are          #
# identified only by party and stored in a         #
# separate database.                               #
####################################################

import sqlite3
import os.path
import re
from nltk.tokenize import sent_tokenize

candidate_database_filename = "speeches.db"
sentence_database_filename = "sentences.db"

# Error checking for candidate database file existence
if not os.path.isfile(candidate_database_filename):
    print("\nError. '{0}' file not found. Exiting.\n".format(candidate_database_filename))
    exit(-1)

# Error checking for sentence database file existence
if os.path.isfile(sentence_database_filename):
    answer = raw_input("Database '{0}' already exists. Are you sure you want to delete and re-create it? (y/n): ".format(sentence_database_filename)).lower()
    if (answer == 'y' or answer == 'yes'):
        print("Re-creating database.\n")
        os.remove(sentence_database_filename)
    else:
        print("Exiting.\n")
        exit(-1)

# Access the candidate SQL file
conn = sqlite3.connect(candidate_database_filename)
c = conn.cursor()
c.execute('SELECT * FROM speeches;')
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

demoCount = 0
repubCount = 0

for i in range(len(speeches)):

    # Remove anything within brackets [*] and parenthesis (*)
    speeches[i] = re.sub("[\(\[].*?[\)\]]", "", speeches[i])
    
    # Remove any word that is all caps. The reasoning is that
    # in this dataset, all capital words are speaker names when
    # the speeches come from interviews.
    speeches[i] = (' ').join([x for x in speeches[i].split(' ') if not x.isupper()])

    sentences = sent_tokenize(speeches[i])

    if parties[i] == "Democratic":
        demoCount += 1
        for sentence in sentences:
            democratic_sentences.append(sentence)

    elif parties[i] == "Republican":
        repubCount +=1
        for sentence in sentences:
            republican_sentences.append(sentence)

    else:
        print("ERROR! Invalid party {0}".format(parties[i]))

print "Dem: {0}\nRep: {1}".format(demoCount, repubCount)

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
