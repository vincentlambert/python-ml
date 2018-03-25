# pylint: disable=too-many-instance-attributes
# pylint: disable=invalid-name

from neural_network import *

class Bird:
    def __init__(self, canvas, x, y, parent_a=None, parent_b=None):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = 30
        self.gravity = 1
        self.velocity = 0
        self.drag = 0.1
        self.lift = 15
        self.fill_color = '#0000FF'
        self.fitness = -1
        self.gx_proxy = canvas.create_oval(self.x - self.size / 2,
                                           self.y - self.size / 2,
                                           self.x + self.size / 2,
                                           self.y + self.size / 2,
                                           fill=self.fill_color)
        if (parent_a is not None) and (parent_b is not None):
            self.brain = NeuralNetwork(2, 6, 1, parent_a.brain, parent_b.brain, mutation_rate=0.01)
        else:
            self.brain = NeuralNetwork(2, 6, 1)

    def destroy(self):
        self.canvas.delete(self.gx_proxy)

    def __str__(self):
        return 'Bird [fitness: %s]' % self.fitness

    def draw(self):
        self.canvas.coords(self.gx_proxy,
                           self.x - self.size / 2,
                           self.y - self.size / 2,
                           self.x + self.size / 2,
                           self.y + self.size / 2)
        self.canvas.itemconfig(self.gx_proxy, fill=self.fill_color)
        # self.fill_color = '#0000FF'

    def update(self, frame_count):
        if self.fitness == -1:
            self.velocity += self.gravity
            self.velocity *= (1 - self.drag)
            self.y += self.velocity
            if self.y > self.canvas.height:
                self.y = self.canvas.height
                self.hit(frame_count)
            if self.y < 0:
                self.y = 0
                self.hit(frame_count)
        else:
            self.x -= self.canvas.speed

    def up(self):
        self.velocity -= self.lift

    def hit(self, fitness):
        self.fitness = fitness
        self.fill_color = '#FF0000'

    def is_hit(self):
        return self.fitness >= 0

    def guess(self, pipe):
        info_vector = [min(pipe.x + pipe.width, self.canvas.width) / self.canvas.width, (pipe.center - self.y) / self.canvas.width]
        action = self.brain.predict(info_vector).item()
        #action = random.random()
        #print('Prediction : %s' % action)
        if action > 0.5:
            #print('Go up !')
            self.up()
