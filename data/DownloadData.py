####################################################
# This script downloads each candidate's speeches  #
# and stores them in a sqlite database.            #
####################################################

from bs4 import BeautifulSoup
import urllib
import re
import sqlite3
import os.path

links_filename = "links.txt"
database_filename = "speeches.db"

class Candidate():

    def __init__(self, name, party, year, all_speeches_url):
        self.name = name
        self.party = party
        self.year = year
        self.all_speeches_url = all_speeches_url

    def downloadSpeeches(self):

        # Store all of the speech links
        self.speech_links = []
        baseURL = "http://www.presidency.ucsb.edu"
        r = urllib.urlopen(self.all_speeches_url).read()
        soup = BeautifulSoup(r)

        for result in soup.find_all("td"):
            for relative_link in result.find_all("a", href = re.compile(r'.*ws\/index.php*'), attrs={'class': None}):
                link = baseURL +  relative_link.get('href').split('..')[1]
                self.speech_links.append(link)

        # Fixes bug where each speech is saved 3 times
        self.speech_links_set = set(self.speech_links)

        # Store the text of each speech
        self.speeches = []

        for speech in self.speeches:
            print speech

        for link in self.speech_links_set:
            r = urllib.urlopen(link).read()
            speech_text = (BeautifulSoup(r).find_all("span", attrs={'class': "displaytext"})[0].getText()).encode("ascii", "ignore")
            self.speeches.append(speech_text)
            print("Downloaded speech #{0} from {1} from {2}".format(len(self.speeches), self.name, self.year))


# Error checking for links file existence
if not os.path.isfile(links_filename):
    print("\nError. '{0}' file not found. Exiting.\n".format(links_filename))
    exit(-1)

# Error checking for database file existence
if os.path.isfile(database_filename):
    answer = raw_input("Database '{0}' already exists. Are you sure you want to delete and re-create it? This will take ~11 minutes. (y/n): ".format(database_filename)).lower()
    if (answer == 'y' or answer == 'yes'):
        print("Re-creating database.\n")
        os.remove(database_filename)
    else:
        print("Exiting.\n")
        exit(-1)

lines = [line.rstrip('\n') for line in open(links_filename)]

# Store each part of each entry separately
names = lines[::6]
parties = lines[1::6]
years = lines[2::6]
speech_types = lines[3::6]
links = lines[4::6]

# Create Candidate objects and give them basic properties
candidates = []
for i in range(len(names)):
    c = Candidate(names[i], parties[i], years[i], links[i])
    candidates.append(c)

# Get each candidate's speeches and store their links to an array in the Candidate object
for c in candidates:
    c.downloadSpeeches()
    print("Downloaded speeches from {0} from {1}".format(c.name, c.year))

# Create the SQL table
conn = sqlite3.connect(database_filename)
c = conn.cursor()
c.execute('''CREATE TABLE speeches (name text, party text, year integer, speech text)''')

# Insert each speech for each candidate into the SQL table
for candidate in candidates:
    for speech in candidate.speeches:
        c.execute("INSERT INTO speeches VALUES (?, ?, ?, ?)", (candidate.name, candidate.party, candidate.year, speech))
    print("Saved speeches to database from {0} from {1}".format(candidate.name, candidate.year))

conn.commit()
conn.close()
