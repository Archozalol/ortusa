import nltk
from nltk.stem.lancaster import LancasterStemmer

import numpy
import tflearn
import tensorflow as tf
import random
import json
import pickle

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # NEW

app = FastAPI()

# NEW
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stemmer = LancasterStemmer()
docs_x = []
docs_y = []

with open("intents.json", "r", encoding="utf-8-sig") as file:  # Opens file as .json file
    data = json.load(file)
try:  # This will try to open saved data so that it doesn't have to go through the entire code every single time
    with open("data.pickle", "rb") as f:  # Saves data as bytes
        words, labels = pickle.load(
            f)  # save all 4 variables in the pickle file
except:  # We're not gonna do any of this if "try" works successfully
    words = []
    labels = []


for intent in data["intents"]:  # Goes through each dictionary
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])

# This part creates a "bag", that takes all the words
# Changes letters into lowercase and removes "?"
words = [stemmer.stem(w.lower()) for w in words if w not in "?"]
# Takes all the words, checks if there's duplicates, and then transforms them back into a list
words = sorted(list(set(words)))

labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []

    wrds = [stemmer.stem(w) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1  # Searches for tags and adds 1

    training.append(bag)
    output.append(output_row)

training = numpy.array(training)
output = numpy.array(output)  # Takes lists and feeds into module

with open("data.pickle", "wb") as f:
    pickle.dump((words, labels), f)  # Saves the data
tf.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])  # This is our input
# Connected to neural data , inputs connect to the 8 neurons
net = tflearn.fully_connected(net, 8)
# The previous 8 neurons connect to these 8 neurons
net = tflearn.fully_connected(net, 8)
# Softmax gives a probability of each neuron in this layer
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)
model = tflearn.DNN(net)

try:
    model.load("model.tflearn")  # Skips re-training
    print("model loaded successfully")
except:
    # This is the AI aspect
    print("model loading failed, retraining model")
    model = tflearn.DNN(net)
    model.fit(training, output, n_epoch=200, batch_size=8, show_metric=True)
    model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]  # create a blank bag of words list
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:  # if word in words list is equal to word in our sentence
                bag[i] = (1)

    return numpy.array(bag)


def learn(c):
    # Pass training data 250 times to increase accuracy (training data is the intents file.)
    tf.compat.v1.reset_default_graph()

    net = tflearn.input_data(
        shape=[None, len(training[0])])  # This is our input
    # Connected to neural data , inputs connect to the 8 neurons
    net = tflearn.fully_connected(net, 8)
    # The previous 8 neurons connect to these 8 neurons
    net = tflearn.fully_connected(net, 8)
    # Softmax gives a probability of each neuron in this layer
    net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
    net = tflearn.regression(net)
    model = tflearn.DNN(net)
    model.fit(training, output, n_epoch=c, batch_size=8, show_metric=True)
    model.save("model.tflearn")


current_course = ""


def ask_question(input):
    global current_course
    input = input.lower()

    first_word = input.split()[0]
    if first_word == "daap" or first_word == "3d" or first_word == "datdiz" or first_word == "graf":
        # Set first word of the message as course(if unset)
        current_course = first_word
        # Remove course from input to prevent double course
        input.replace(current_course+" ", "")

    results = model.predict(
        [bag_of_words(current_course + " " + input, words)])[0]
    # Give us the index of the greatest value in the list
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    response = ""
    if results[results_index] > 0.7:

        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        response = random.choice(responses)
    else:
        response = "Atvainojos, bet es nesapratu jautājumu."
    if current_course != "":
        return current_course.upper()+": "+response
    else:
        return response


@app.get("/restart")
def restart():
    global current_course
    current_course = ""


@app.get("/train")
def train(c: int):
    learn(c)
    return "Modeļa apmācība pabeigta veiksmīgi!"


@app.get("/ask")
def question(q: str):
    return ask_question(q)


@app.get("/course")
def get_course():
    return current_course
