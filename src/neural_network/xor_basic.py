#
# Basic XOR with NEural Network
#
from neural_network import *


def test_nn(neural_networl):
    print(neural_networl.predict([1, 0]))
    print(neural_networl.predict([0, 1]))
    print(neural_networl.predict([1, 1]))
    print(neural_networl.predict([0, 0]))


def train_nn(neural_networl, iterations):
    data = [
        {
            'inputs': [1, 0],
            'target': [1]
        },
        {
            'inputs': [0, 1],
            'target': [1]
        },
        {
            'inputs': [1, 1],
            'target': [0]
        },
        {
            'inputs': [0, 0],
            'target': [0]
        },
    ]

    for _ in range(iterations):
        rand_choice = random.choice(data)
        neural_networl.train(rand_choice['inputs'], rand_choice['target'])


#
# Main
#
if __name__ == '__main__':
    print("*****")
    print("***** Main...")
    print("*****")

    # Basic tests
    # nn = NeuralNetwork(2, 2, 2)
    # inputs = np.array([1, 0])
    # targets = np.array([1, 1])
    # nn.train(inputs, targets)

    # Neural network training for XOR
    NN = NeuralNetwork(2, 3, 1)
    print('***** Before training')
    test_nn(NN)
    train_nn(NN, 100000)
    print('***** After training')
    test_nn(NN)
