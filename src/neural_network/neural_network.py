#
# Neural Network
#
import random as random
import numpy as np

# pylint: disable=too-many-instance-attributes
# pylint: disable=invalid-name


class NeuralNetwork:
    '''NeuralNetwork'''

    def __init__(self, input_nodes=0, hidden_nodes=0, output_nodes=0, parent_a=None, parent_b=None, mutation_rate=0):
        if(parent_a is not None) and (parent_b is not None):
            self.learning_rate = parent_a.learning_rate
            self.input_nodes = parent_a.input_nodes
            self.hidden_nodes = parent_a.hidden_nodes
            self.output_nodes = parent_a.output_nodes
            self._mix_and_mutate(parent_a, parent_b, mutation_rate)
        else:
            self.learning_rate = 0.1
            self.input_nodes = input_nodes
            self.hidden_nodes = hidden_nodes
            self.output_nodes = output_nodes
            self.weights_ih = np.matrix(np.random.random(
                (self.hidden_nodes, self.input_nodes))) / self.input_nodes
            self.weights_ho = np.matrix(np.random.random(
                (self.output_nodes, self.hidden_nodes))) / self.hidden_nodes
            self.bias_h = np.matrix(np.random.random(
                (self.hidden_nodes, 1))) / self.input_nodes
            self.bias_o = np.matrix(np.random.random(
                (self.output_nodes, 1))) / self.hidden_nodes

    def __str__(self):
        return 'NeuralNetwork[%s, %s, %s] :\n  Hidden : \n%s\n  Ouput : \n%s' % (self.input_nodes, self.hidden_nodes, self.output_nodes, self.weights_ih, self.weights_ho)

    def clone(self):
        new_neural_network = NeuralNetwork(
            self.input_nodes, self.hidden_nodes, self.output_nodes)
        new_neural_network.weights_ih = self.weights_ih.copy()
        new_neural_network.weights_ho = self.weights_ho.copy()
        new_neural_network.bias_h = self.bias_h.copy()
        new_neural_network.bias_o = self.bias_o.copy()
        new_neural_network.learning_rate = self.learning_rate
        return new_neural_network

    def get_dna(self):
        to_dna = list()
        to_dna.append(np.array(self.weights_ih).flatten())
        to_dna.append(np.array(self.weights_ho).flatten())
        to_dna.append(np.array(self.bias_h).flatten())
        to_dna.append(np.array(self.bias_o).flatten())
        return np.concatenate(to_dna)

    def set_dna(self, dna):
        self.weights_ih = np.matrix(
            dna[:(self.input_nodes*self.hidden_nodes)]).reshape(self.hidden_nodes, self.input_nodes)
        dna = dna[(self.input_nodes*self.hidden_nodes):]
        self.weights_ho = np.matrix(
            dna[:(self.hidden_nodes*self.output_nodes)]).reshape(self.output_nodes, self.hidden_nodes)
        dna = dna[(self.hidden_nodes*self.output_nodes):]
        self.bias_h = np.matrix(dna[:self.hidden_nodes]).reshape(
            self.hidden_nodes, 1)
        dna = dna[self.hidden_nodes:]
        self.bias_o = np.matrix(dna[:self.output_nodes]).reshape(
            self.output_nodes, 1)
        dna = dna[self.output_nodes:]

    def _mix_and_mutate(self, parent_a, parent_b, mutation_rate):
        dna_a = parent_a.get_dna()
        dna_b = parent_b.get_dna()
        split = random.randint(0, len(dna_a))
        dna = np.concatenate((dna_a[0:split], dna_b[split:len(dna_a)]))

        for x in np.nditer(dna, op_flags=['readwrite']):
            if random.random() < mutation_rate:
                x[...] = random.random()

        self.set_dna(dna)

    # def mutate(self, rate):
    #     for x in np.nditer(self.weights_ih, op_flags=['readwrite']):
    #         if random.random() < rate:
    #             x[...] = random.random()
    #     for x in np.nditer(self.weights_ho, op_flags=['readwrite']):
    #         if random.random() < rate:
    #             x[...] = random.random()
    #     for x in np.nditer(self.bias_h, op_flags=['readwrite']):
    #         if random.random() < rate:
    #             x[...] = random.random()
    #     for x in np.nditer(self.bias_o, op_flags=['readwrite']):
    #         if random.random() < rate:
    #             x[...] = random.random()

    def set_to(self, value=0):
        for x in np.nditer(self.weights_ih, op_flags=['readwrite']):
            x[...] = value
        for x in np.nditer(self.weights_ho, op_flags=['readwrite']):
            x[...] = value
        for x in np.nditer(self.bias_h, op_flags=['readwrite']):
            x[...] = value
        for x in np.nditer(self.bias_o, op_flags=['readwrite']):
            x[...] = value

    def predict(self, input_data):
        ''' Feed forward function '''
        inputs = np.matrix(input_data).transpose()

        # Generating hidden layer values
        # hidden = np.dot(self.weights_ih, inputs.reshape(inputs.size, 1))

        hidden = self.weights_ih * inputs
        # hidden = np.add(hidden, self.bias_h)
        hidden = hidden + self.bias_h
        # hidden = np.array([self.sigmoid(x) for x in hidden])
        hidden = np.matrix(np.array([self.sigmoid(x)
                                     for x in hidden])).transpose()

        # Generating outputs layer values
        # outputs = np.dot(self.weights_ho, hidden)
        outputs = self.weights_ho * hidden
        # outputs = np.add(outputs, self.bias_o)
        outputs = outputs + self.bias_o
        # outputs = np.array([self.sigmoid(x) for x in outputs])
        outputs = np.matrix(np.array([self.sigmoid(x)
                                      for x in outputs])).transpose()

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
        hidden = np.matrix(np.array([self.sigmoid(x)
                                     for x in hidden])).transpose()

        # Generating outputs layer values
        # outputs = np.dot(self.weights_ho, hidden)
        outputs = self.weights_ho * hidden
        # outputs = np.add(outputs, self.bias_o)
        outputs = outputs + self.bias_o
        # outputs = np.array([self.sigmoid(x) for x in outputs])
        outputs = np.matrix(np.array([self.sigmoid(x)
                                      for x in outputs])).transpose()

        #
        # Back propagation
        #

        # Output layer error
        errors_o = targets - outputs
        # Calculate output gradient
        output_gradients = np.matrix(
            np.array([self.desigmoid(x) for x in outputs])).transpose()
        output_gradients = np.multiply(
            output_gradients, errors_o) * self.learning_rate
        # Adjust output bias
        self.bias_o += output_gradients
        # Calculate deltas
        weights_ho_deltas = output_gradients * hidden.transpose()
        # Adjust hidden->output weights
        self.weights_ho += weights_ho_deltas

        # Hidden layer error
        errors_h = np.dot(self.weights_ho.transpose(), errors_o)
        # Calculate hidden gradient
        hidden_gradients = np.matrix(
            np.array([self.desigmoid(x) for x in hidden])).transpose()
        hidden_gradients = np.multiply(
            hidden_gradients, errors_h) * self.learning_rate
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


#
# Main
#
if __name__ == '__main__':
    print("*****")
    print("***** Main...")
    print("*****")

    NN_A = NeuralNetwork(3, 5, 2)
    NN_A.set_to(0)
    # print(NN_A)
    # NN_B = NN_A.clone()
    # NN_A.mutate(0.5)
    # print(NN_B)
    # print(NN_A)

    NN_B = NeuralNetwork(3, 5, 2)
    NN_B.set_to(1)
    # NN_B.set_dna(NN_A.get_dna())

    # dna_a = NN_A.get_dna()
    # dna_b = NN_B.get_dna()
    # split = random.randint(0, len(dna_a))
    # dna = np.concatenate((dna_a[0:split], dna_b[split:len(dna_a)]))

    # print(dna_a)
    # print('----------')
    # print(dna_b)
    # print('----------')
    # print(dna)

    # print(NN_A)
    # print('----------')
    NN_C = NeuralNetwork(parent_a=NN_A, parent_b=NN_B, mutation_rate=0.01)
    print(NN_C)
