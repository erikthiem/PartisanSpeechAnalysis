import sys
import sqlite3
import os
import numpy as np

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

def generateWordCountMatrix(training_sentences):
    # TODO
    pass


def generatePartyVector(training_sentences):
    # TODO
    pass

def train(training_sentences, num_iterations):
    # TODO 

    for iteration in range(num_iterations):
        print iteration


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

    # TODO: Generate "X[sentence_id, word_id] = word_count" sparse matrix
    X = generateWordCountMatrix(training_sentences)

    # TODO: Generate "Y[sentence_id] = party" vector
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
