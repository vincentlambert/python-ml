#
# Perceptron
#
from random import uniform

LEARNING_RATE = 0.001
CONST_A = uniform(0, 10)
CONST_B = uniform(-0.5, 0.5)

def f(x):
    return CONST_A * x + CONST_B

def translateX(value):
    return int(-value * 200 + 200)

def translateY(value):
    return int(value * 200 + 200)

#
# Perceptron
#
class Perceptron:
    ''' Perceptron '''
    def __init__(self, array_size, canvas=None):
        self.canvas = canvas
        self.neuron = Neuron()
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
class Neuron:
    def __init__(self):
        self.weights = [uniform(-1, 1), uniform(-1, 1)]
        self.bias = uniform(-1, 1)
    
    def guess(self, inputs):
        sum = self.bias
        for i in range(len(self.weights)):
            sum += inputs[i] * self.weights[i]
        if(sum >= 0):
            return 1
        return -1

    def learn(self, error):
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
            fill_color = '#0000FF'
            if self.label == 1: #self.cheked:
                fill_color = '#00FF00'
            self.gx_proxy = self.canvas.create_oval(translateX(self.x)-self.r, translateY(self.y)-self.r, translateX(self.x)+self.r, translateY(self.y)+self.r, fill=fill_color)
    
    def draw(self):
        if self.canvas is not None:
            fill_color = '#0000FF'
            if self.label == 1: #self.cheked:
                fill_color = '#00FF00'
            self.canvas.coords(self.gx_proxy, translateX(self.x)-self.r, translateY(self.y)-self.r, translateX(self.x)+self.r, translateY(self.y)+self.r)
            self.canvas.itemconfig(self.gx_proxy, fill=fill_color)
        else:
            print('Point[%s, %s, %s] : %s' % (self.x, self.y, self.label, self.cheked))
