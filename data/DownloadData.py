####################################################
# This script downloads each candidate's speeches. #
####################################################

from bs4 import BeautifulSoup
import urllib
import re

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
            speech_text = BeautifulSoup(r).find_all("span", attrs={'class': "displaytext"})[0].getText()
            self.speeches.append(speech_text)

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
print candidates[40].name
candidates[40].downloadSpeeches()

# TODO: Create a sqlite table to hold the candidates[] array
