####################################################
# This script downloads each candidate's speeches. #
####################################################

class Candidate():

    def __init__(self, name, party, year, speeches_url):
        self.name = name
        self.party = party
        self.year = year
        self.speeches_url = speeches_url


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

# TODO: Get each candidate's speeches and store their links to an array in the Candidate object

# TODO: Download the plaintext of each speech and store each as an array entry in the Candidate object

# TODO: Create a sqlite table to hold the candidates[] array
