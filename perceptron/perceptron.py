import sys
import sqlite3
import os
import numpy
from scipy.sparse import lil_matrix
from collections import defaultdict

class Sentence():
    
    def __init__(self, party, text):
        self.party = party
        self.text = text


def sentencesFromDB(db_file_path):

    conn = sqlite3.connect(db_file_path)
    c = conn.cursor()
    c.execute('SELECT * FROM sentences;')
    results = c.fetchall()
    conn.commit()
    conn.close() 

    sentences = [] 
    for r in results:
        s = Sentence(r[0], r[1])
        sentences.append(s)

    return sentences


# Generate "X[sentence_id, word_id] = word_count" sparse matrix
def generateWordCountMatrix(training_sentences):

    sentence_word_frequencies = []

    # Create a dictionary to store all words in order to get vocabulary size
    all_word_dict = defaultdict(int)

    for sentence in training_sentences:
        words = sentence.text.lower().split(" ")
        word_frequencies = {w:words.count(w) for w in set(words)}
        sentence_word_frequencies.append(word_frequencies)
        for word in words:
            all_word_dict[word] += 1

    # Create dictionaries to do "word" -> "word ID" and "word ID" -> "word"
    word_to_id = {}
    id_to_word = {}
    word_id = 0
    for word in all_word_dict.iteritems():
        word_to_id[word[0]] = word_id
        id_to_word[word_id] = word[0]
        word_id += 1

    # Create blank X matrix
    X = lil_matrix( (len(training_sentences), len(all_word_dict)))

    # Populate X matrix with the values from the word frequencies in each sentence
    for sentence in range(len(sentence_word_frequencies)):
        for word, frequency in sentence_word_frequencies[sentence].iteritems():
            X[sentence, word_to_id[word]] = frequency

    # Convert X to sparse CSR format
    X = X.tocsr()

    print X.shape

    return X


# Generate "Y[sentence_id] = party" vector
def generatePartyVector(training_sentences):

    Y = numpy.zeros((len(training_sentences), 1), dtype=int)
    
    for sentence in range(len(training_sentences)):
        if training_sentences[sentence].party == "Democratic":
            Y[sentence] = 1
        else:
            Y[sentence] = 0

    return Y


def train(X, num_iterations):
    # TODO 
    pass


def predict(testing_sentences, weights):
    # TODO
    return []
    pass


def percentSimilar(list1, list2):

    total = len(list1)
    count_similar = 0

    for i in range(len(list1)):
        if list1[i] == list2[i]:
            count_similar += 1

    return float(count_similar) / total


if __name__ == "__main__":

    if len(sys.argv) != 4:
        print "\nError! Expected syntax: 'python perceptron.py training_db_path testing_db_path num_iterations'\n"
        sys.exit(-1)

    training_data_path = sys.argv[1]
    testing_data_path = sys.argv[2]
    num_iterations = int(sys.argv[3])

    if not os.path.isfile(training_data_path):
        print "Error! Training database {0} does not exist.\n".format(training_data_path)
        exit(-1)

    if not os.path.isfile(testing_data_path):
        print "Error! Testing database {0} does not exist.\n".format(testing_data_path)
        exit(-1)

    # Load the Training data
    training_sentences = sentencesFromDB(training_data_path)

    # Generate "X[sentence_id, word_id] = word_count" sparse matrix
    X = generateWordCountMatrix(training_sentences)

    # Generate "Y[sentence_id] = party" vector
    Y = generatePartyVector(training_sentences)

    # Note: both of these are modeled after the 5525 HW1, Preceptron assignment

    weights = train(training_sentences, num_iterations)

    # Load the testing data
    testing_sentences = sentencesFromDB(testing_data_path)

    # Predict each of the testing sentences
    predicted_classifications = predict(testing_sentences, weights)

    # Determine accuracy of predictions
    correct_classifications = [s.party for s in testing_sentences]
    #accuracy = percentSimilar(predicted_classifications, correct_classifications)
    #print("Accuracy: {0}".format(accuracy))
