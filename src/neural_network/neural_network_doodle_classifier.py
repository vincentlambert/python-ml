#
# Neural Network Doodle Classifier
#
import numpy as np
import random
from neural_network import NeuralNetwork

EPOCH = 0

LABEL_CAR = 0
LABEL_CAT = 1
LABEL_BANANA = 2
LABEL_APPLE = 3
LABEL_AIRPLANE = 4

TRAINING_ELTS = 1000
TESTING_ELTS = 100

DATA_SOURCE_BASE_PATH = 'data/quickdraw_dataset/'

DATA_SOURCES = [
    {
        'raw_data_file':'full_numpy_bitmap_car.npy',
        'label':LABEL_CAR
    },
    {
        'raw_data_file':'full_numpy_bitmap_cat.npy',
        'label':LABEL_CAT
    },
    {
        'raw_data_file':'full_numpy_bitmap_banana.npy',
        'label':LABEL_BANANA
    },
    {
        'raw_data_file':'full_numpy_bitmap_apple.npy',
        'label':LABEL_APPLE
    },
    {
        'raw_data_file':'full_numpy_bitmap_airplane.npy',
        'label':LABEL_AIRPLANE
    }
]

training_data = []
testing_data = []

neuralnetwork = NeuralNetwork(784, 64, len(DATA_SOURCES))

def train():
    global EPOCH
    random.shuffle(training_data)
    for i in range(len(training_data)):
        neuralnetwork.train(training_data[i]['prepared_data'], training_data[i]['expected_guess'])
    EPOCH += 1

def test():
    random.shuffle(testing_data)
    score = 0
    for i in range(len(testing_data)):
        results = neuralnetwork.predict(testing_data[i]['prepared_data'])
        if testing_data[i]['label'] == results.argmax():
            score += 1
    return score / len(testing_data)

if __name__ == '__main__':
    print('Started')

    print('Preparing training data...')
    # Preparing training data
    for i in range(len(DATA_SOURCES)):
        data = np.load(DATA_SOURCE_BASE_PATH + DATA_SOURCES[i]['raw_data_file'])
        for j in range(0, TRAINING_ELTS):
            prepared_data = []
            for x in range(len(data[j])):
                prepared_data.append(data[j][x]/255)
            expected = np.zeros(len(DATA_SOURCES))
            expected[DATA_SOURCES[i]['label']] = 1
            training_data.append({'raw_data':data[j], 'label':DATA_SOURCES[i]['label'], 'prepared_data':prepared_data, 'expected_guess':expected})
    random.shuffle(training_data)

    print('Preparing testing data...')
    # Preparing testing data
    for i in range(len(DATA_SOURCES)):
        data = np.load(DATA_SOURCE_BASE_PATH + DATA_SOURCES[i]['raw_data_file'])
        for j in range(TRAINING_ELTS, TRAINING_ELTS + TESTING_ELTS):
            prepared_data = []
            for x in range(len(data[j])):
                prepared_data.append(data[j][x]/255)
            expected = np.zeros(len(DATA_SOURCES))
            expected[DATA_SOURCES[i]['label']] = 1
            testing_data.append({'raw_data':data[j], 'label':DATA_SOURCES[i]['label'], 'prepared_data':prepared_data, 'expected_guess':expected})
    random.shuffle(testing_data)

    print('Data ready')

    command = ''
    while command != 'q':
        command = input('Input command (q:quit, t:train, c:check) : ')
        if command == 't':
            print('Training started...')
            train()
            print('Epoch %s done !' % EPOCH)
        elif command =='c':
            print('Processing test data...')
            print('With result : %.2f' % (test() * 100))
