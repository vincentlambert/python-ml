import random

# pylint: disable=too-many-instance-attributes
# pylint: disable=invalid-name


class Pipe:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = self.canvas.width
        self.width = 40
        self.height = random.randint(100, 200)
        self.center = random.randint(25 + int(self.height / 2), self.canvas.height - 25 - int(self.height / 2))
        self.velocity = 1
        self.fill_color = '#0000FF'
        self.gx_proxy_top = canvas.create_rectangle(self.x,
                                                    0,
                                                    self.x + self.width,
                                                    self.center - self.height / 2,
                                                    fill=self.fill_color)
        self.gx_proxy_bottom = canvas.create_rectangle(self.x,
                                                       self.center + self.height / 2,
                                                       self.x + self.width,
                                                       self.canvas.height,
                                                       fill=self.fill_color)

    def draw(self):
        self.canvas.coords(self.gx_proxy_top,
                           self.x,
                           0,
                           self.x + self.width,
                           self.center - self.height / 2)
        self.canvas.coords(self.gx_proxy_bottom,
                           self.x,
                           self.center + self.height / 2,
                           self.x + self.width,
                           self.canvas.height)

    def update(self):
        self.x -= self.velocity

    def hits(self, bird):
        if (bird.x >= self.x) and (bird.x <= self.x + self.width):
            if (bird.y < self.center - self.height / 2) or (bird.y > self.center + self.height / 2):
                return True
        return False

    def off_screen(self):
        return self.x < (-1 * self.width)