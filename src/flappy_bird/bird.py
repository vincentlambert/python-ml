# pylint: disable=too-many-instance-attributes
# pylint: disable=invalid-name

from neural_network import *

class Bird:
    def __init__(self, canvas, x, y):
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
        self.brain = NeuralNetwork(4, 10, 1)

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
            # TODO: Variabiliser la vitesse de défilement
            self.x -= 1

    def up(self):
        self.velocity -= self.lift

    def hit(self, fitness):
        self.fitness = fitness
        self.fill_color = '#FF0000'

    def is_hit(self):
        return self.fitness >= 0

    def guess(self, dist, h_top, h_botton):
        action = self.brain.predict([self.x, dist, h_top, h_botton]).item()
        # TODO: Activate NN here !
        # if action > 0.5:
        if random.random() > 0.5:
            self.up()
