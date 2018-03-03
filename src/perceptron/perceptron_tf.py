#
# Perceptron made with TensorFlow
#
import tensorflow as tf

# #hello = tf.constant('Hello, TensorFlow!')

# nodeX = tf.placeholder(tf.float32)

# nodeA = tf.Variable(3.0, dtype=tf.float32)
# nodeB = tf.Variable(4.0, dtype=tf.float32)
# #print(nodeA, nodeB)

# nodeY = (nodeA * nodeX) + nodeB

# init = tf.global_variables_initializer()
# sess = tf.Session()
# sess.run(init)
# #print(sess.run([nodeA, nodeB]))
# print(sess.run(nodeY, {nodeX: [0, 1, 2, 3, 4]}))

from random import uniform
import numpy as np

LEARNING_RATE = 0.01
CONST_A = uniform(0, 10)
CONST_B = uniform(-0.5, 0.5)

def f(x):
    return CONST_A * x + CONST_B

def translateX(value):
    return int(-value * 200 + 200)

def translateY(value):
    return int(value * 200 + 200)

def testLinearModel():
    # Training data
    tx_data = np.linspace(-1, 1, 10)
    ty_data = np.vectorize(f)(tx_data)

    # Linear model
    nodeA = tf.Variable(uniform(-1, 1), dtype=tf.float32)
    nodeX = tf.placeholder(tf.float32)
    nodeB = tf.Variable(uniform(-1, 1), dtype=tf.float32)
    nodePred = nodeA * nodeX + nodeB

    # Error value
    nodeY = tf.placeholder(tf.float32)
    squared_deltas = tf.square(nodeY - nodePred)
    loss = tf.reduce_sum(squared_deltas)

    # TS session
    sess = tf.Session()
    init = tf.global_variables_initializer()
    sess.run(init)

    print('***** Before learning *****')
    print('A : %s' % sess.run(nodeA))
    print('B : %s' % sess.run(nodeB))
    print('Linear model : %s' % sess.run(nodePred, {nodeX: 0.0}))
    print('Loss : %s' % sess.run(loss, {nodeX: tx_data, nodeY: ty_data}))

    # Machine learning
    print('***** Learning stage *****')
    optimizer = tf.train.GradientDescentOptimizer(0.01)
    train = optimizer.minimize(loss)
    error = 100
    while error > 1:
        sess.run(train, {nodeX: tx_data, nodeY: ty_data})
        error = sess.run(loss, {nodeX: tx_data, nodeY: ty_data})
        print('Loss : %s' % error)

    print('***** After learning *****')
    print('[%s] A : %s' % (CONST_A, sess.run(nodeA)))
    print('[%s] B : %s' % (CONST_B, sess.run(nodeB)))
    print('Linear model : %s' % sess.run(nodePred, {nodeX: 0.0}))
    print('Loss : %s' % sess.run(loss, {nodeX: tx_data, nodeY: ty_data}))


def testSpacialModel():
    # Training data
    tx_data = np.linspace(-1, 1, 10)
    ty_data = np.linspace(-1, 1, 10)
    tl_data = [None for i in range(len(tx_data))] #= np.empty(len(tx_data), dtype=str)
    for i in range(len(tx_data)):
        tl_data[i] = 'UP' if f(tx_data[i]) >= ty_data[i] else 'DOWN'
    print(tl_data)

if __name__ == '__main__':
    testSpacialModel()

    

#
# Perceptron
#
class PerceptronTF:
    ''' PerceptronTF '''
    def __init__(self, array_size, canvas=None):
        self.canvas = canvas
        self.neuron = NeuronTF()
        self.points = []
        if self.canvas is not None:
            self.errorLabel = self.canvas.create_text(5, 5, text='Current error : -', anchor='nw')
        for i in range(array_size):
            self.points.append(Point(canvas=self.canvas))

    def draw(self):
        for point in self.points:
            point.draw()

    def learn(self):
        errors = self.checkPoints()
        # FIXME: self.neuron.learn(error) for error in errors
        for error in errors:
            self.neuron.learn(error)
        # TODO: valider la gestion des erreurs
        error = sum(abs(x.error) for x in errors)
        if self.canvas is not None:
            self.canvas.itemconfig(self.errorLabel, text='Current error : %s' % error)
        else:
            print('Total error : %s' % error)
        return error
    
    def guessY(self, x):
        w0 = self.neuron.weights[0]
        w1 = self.neuron.weights[1]
        w2 = self.neuron.bias
        return -(w0/w1) * x - (w2/w1)

    def checkPoints(self):
        errors = []
        for point in self.points:
            guess = self.neuron.guess([point.x, point.y])
            point.cheked = (point.label ==  guess)
            errors.append(Error([point.x, point.y], point.label-guess))
        return errors

#
# Neuron
#
class NeuronTF:
    def __init__(self):
        self.nodeX0 = tf.placeholder(tf.float32)
        self.nodeW0 = tf.Variable(uniform(-1, 1), dtype=tf.float32)
        self.nodeX1 = tf.placeholder(tf.float32)
        self.nodeW1 = tf.Variable(uniform(-1, 1), dtype=tf.float32)
        self.bias = tf.Variable(uniform(-1, 1), dtype=tf.float32)

        self.target = tf.Variable(uniform(-1, 1), dtype=tf.float32)
        self.nodeY = (self.nodeW0 * self.nodeX0) + (self.nodeW1 * self.nodeX1) + self.bias
        self.squared_deltas = tf.square(self.nodeY - self.target)
        self.loss = tf.reduce_sum(self.squared_deltas)
        self.init = tf.global_variables_initializer()
        self.sess = tf.Session()
        self.sess.run(self.init)

        self.optimizer = tf.train.GradientDescentOptimizer(LEARNING_RATE)
        self.train = self.optimizer.minimize(self.loss)
# #print(sess.run([nodeA, nodeB]))
# print(sess.run(nodeY, {nodeX: [0, 1, 2, 3, 4]}))
    
    def guess(self, inputs):
        sum = self.sess.run(self.nodeY, {self.nodeX0 : inputs[0], self.nodeX1 : inputs[1]})
        if(sum >= 0):
            return 1
        return -1

    def learn(self, error):
        x_data = np.linspace(-1, 1, 10)
        vf = np.vectorize(f)
        y_data = vf(x_data)

        self.sess.run(self.train, {})
        self.bias += error.error * LEARNING_RATE
        for i in range(len(self.weights)):
            self.weights[i] += error.inputs[i] * error.error * LEARNING_RATE
    
#
# Error
#
class Error:
    def __init__(self, inputs, error):
        self.inputs = inputs
        self.error = error

#
# Point
#
class Point:
    def __init__(self, x=None, y=None, canvas=None):
        self.canvas = canvas
        self.r = 5
        self.cheked = False

        if x is None:
            self.x = uniform(-1, 1)
        else:
            self.x = x

        if y is None:
            self.y = uniform(-1, 1)
        else:
            self.y = y

        if self.y >= f(self.x):
            self.label = 1
        else:
            self.label = -1

        if self.canvas is not None:
            fill_color = '#FF0000'
            if self.cheked:
                fill_color = '#00FF00'
            self.gx_proxy = self.canvas.create_oval(translateX(self.x)-self.r, translateY(self.y)-self.r, translateX(self.x)+self.r, translateY(self.y)+self.r, fill=fill_color)
    
    def draw(self):
        if self.canvas is not None:
            fill_color = '#FF0000'
            if self.cheked:
                fill_color = '#00FF00'
            self.canvas.coords(self.gx_proxy, translateX(self.x)-self.r, translateY(self.y)-self.r, translateX(self.x)+self.r, translateY(self.y)+self.r)
            self.canvas.itemconfig(self.gx_proxy, fill=fill_color)
        else:
            print('Point[%s, %s, %s] : %s' % (self.x, self.y, self.label, self.cheked))
