#
# Neural Network
#
import numpy as np
import random as random

class NeuralNetwork:
    '''NeuralNetwork'''
    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes
        self.weights_ih = np.matrix(np.random.random((self.hidden_nodes, self.input_nodes)))
        self.weights_ho = np.matrix(np.random.random((self.output_nodes, self.hidden_nodes)))
        self.bias_h = np.matrix(np.random.random((self.hidden_nodes, 1)))
        self.bias_o = np.matrix(np.random.random((self.output_nodes, 1)))
        self.learning_rate = 0.1

    def __str__(self):
        return 'NeuralNetwork[%s, %s, %s] :\n  Hidden : \n%s\n  Ouput : \n%s' % (self.input_nodes, self.hidden_nodes, self.output_nodes, self.weights_ih, self.weights_ho)
    
    def predict(self, input_data):
        ''' Feed forward function '''
        inputs = np.matrix(input_data).transpose()

        # Generating hidden layer values
        # hidden = np.dot(self.weights_ih, inputs.reshape(inputs.size, 1))
        hidden = self.weights_ih * inputs
        # hidden = np.add(hidden, self.bias_h)
        hidden = hidden + self.bias_h
        # hidden = np.array([self.sigmoid(x) for x in hidden])
        hidden = np.matrix(np.array([self.sigmoid(x) for x in hidden])).transpose()

        # Generating outputs layer values
        # outputs = np.dot(self.weights_ho, hidden)
        outputs = self.weights_ho * hidden
        # outputs = np.add(outputs, self.bias_o)
        outputs = outputs + self.bias_o
        # outputs = np.array([self.sigmoid(x) for x in outputs])
        outputs = np.matrix(np.array([self.sigmoid(x) for x in outputs])).transpose()

        return outputs.flatten()

    def train(self, input_data, target_data):
        ''' Train function  (feed forward and back propagation)'''
        # outputs = self.predict(inputs)
        # # Output layer error
        # errors_o = targets - outputs
        # print(errors_o)
        # # Hidden layer error
        # errors_h = np.dot(self.weights_ho.transpose(), errors_o)
        # print(errors_h)
        # # Input layer error
        # errors_i = np.dot(self.weights_ih.transpose(), errors_h)
        # print(errors_i)

        inputs = np.matrix(input_data).transpose()
        targets = np.matrix(target_data).transpose()

        #
        # Feed forward
        #

        # Generating hidden layer values
        # hidden = np.dot(self.weights_ih, inputs.reshape(inputs.size, 1))
        hidden = self.weights_ih * inputs
        # hidden = np.add(hidden, self.bias_h)
        hidden = hidden + self.bias_h
        # hidden = np.array([self.sigmoid(x) for x in hidden])
        hidden = np.matrix(np.array([self.sigmoid(x) for x in hidden])).transpose()

        # Generating outputs layer values
        # outputs = np.dot(self.weights_ho, hidden)
        outputs = self.weights_ho * hidden
        # outputs = np.add(outputs, self.bias_o)
        outputs = outputs + self.bias_o
        # outputs = np.array([self.sigmoid(x) for x in outputs])
        outputs = np.matrix(np.array([self.sigmoid(x) for x in outputs])).transpose()

        #
        # Back propagation
        #

        # Output layer error
        errors_o = targets - outputs
        # Calculate output gradient
        output_gradients = np.matrix(np.array([self.desigmoid(x) for x in outputs])).transpose()
        output_gradients = np.multiply(output_gradients, errors_o) * self.learning_rate
        # Adjust output bias
        self.bias_o += output_gradients
        # Calculate deltas
        weights_ho_deltas = output_gradients * hidden.transpose()
        # Adjust hidden->output weights
        self.weights_ho += weights_ho_deltas

        # Hidden layer error
        errors_h = np.dot(self.weights_ho.transpose(), errors_o)
        # Calculate hidden gradient
        hidden_gradients = np.matrix(np.array([self.desigmoid(x) for x in hidden])).transpose()
        hidden_gradients = np.multiply(hidden_gradients, errors_h) * self.learning_rate
        # Adjust hidden bias
        self.bias_h += hidden_gradients
        # Calculate deltas
        weights_ih_deltas = hidden_gradients * inputs.transpose()
        # Adjust input->hidden weights
        self.weights_ih += weights_ih_deltas


    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def desigmoid(y):
        # return sigmoid(x) * (1 - sigmoid(x))
        return y * (1 - y)


def testNN(nn):
    print(nn.predict([1, 0]))
    print(nn.predict([0, 1]))
    print(nn.predict([1, 1]))
    print(nn.predict([0, 0]))

def trainNN(nn, iterations):
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
        x = random.choice(data)
        nn.train(x['inputs'], x['target'])

#
# Draw heatmap
#
import matplotlib.pyplot as plt

def draw_heatmap(neural_network):
    step = 10
    data = []
    labels = []

    for i in range(0, step + 1):
        labels.append(i / step)

    for x1 in range(0, step + 1):
        data.append([])
        for x2 in range(0, step + 1):
            data[x1].append(neural_network.predict([x1 / step, x2 / step]).item())

    # Mode 1
    # fig, axis = plt.subplots()
    # heatmap = axis.pcolor(data, cmap=plt.cm.Greys)
    # axis.set_title('Network response')
    # print(repr(fig))
    # print(repr(axis))

    # Mode 2
    x, y = np.meshgrid(labels, labels)
    intensity = np.array(data)
    plt.pcolormesh(x, y, intensity, cmap=plt.cm.YlOrRd)
    plt.colorbar()

    plt.show()

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
    nn = NeuralNetwork(2, 3, 1)
    print('***** Before training')
    testNN(nn)
    trainNN(nn, 100000)
    print('***** After training')
    testNN(nn)

    # Plot heatmap
    draw_heatmap(nn)