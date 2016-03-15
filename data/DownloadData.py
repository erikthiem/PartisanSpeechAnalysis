####################################################
# This script downloads each candidate's speeches  #
# and stores them in a sqlite database.            #
####################################################

from bs4 import BeautifulSoup
import urllib
import re
import sqlite3

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

        # Store the text of each speech
        self.speeches = []

        for link in self.speech_links:
            r = urllib.urlopen(link).read()
            speech_text = (BeautifulSoup(r).find_all("span", attrs={'class': "displaytext"})[0].getText()).encode("ascii", "ignore")
            self.speeches.append(speech_text)
            print("Downloaded speech #{0} from {1}".format(len(self.speeches), self.name))

# Open file
filename = "links.txt"
lines = [line.rstrip('\n') for line in open(filename)]

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
# TODO: Set to download all candidates speeches, not just candidates[40] (this is in here right now for debugging/developing because it takes
#       a while to download all of the speeches
for c in candidates:
    c.downloadSpeeches()
    print("Downloaded speeches from {0}".format(c.name))

# TODO: Extend this to all candidates and all of their speeches
# TODO: Add some checking so an existing table isn't accidentally overwritten.
conn = sqlite3.connect('speeches.db')
c = conn.cursor()
c.execute('''CREATE TABLE speeches (name text, party text, year integer, speech text)''')

for candidate in candidates:
    for speech in candidate.speeches:
        c.execute("INSERT INTO speeches VALUES (?, ?, ?, ?)", (candidate.name, candidate.party, candidate.year, speech))
    print("Saved speeches to database from {0}".format(candidate.name))

conn.commit()
conn.close()
