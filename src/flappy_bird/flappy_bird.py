import sys
sys.path.append('./src/neural_network')

from tkinter import *
import platform

from bird import *
from pipe import *



'''
Flappy Bird
'''
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-ancestors


class FlappyBirdApp(Canvas):
    def __init__(self, root, width, height):
        Canvas.__init__(self, root, width=width, height=height)
        self._root_app = root
        self._running = False
        self._bird_offset = 100
        self.width = width
        self.height = height
        self.frame_count = 0
        self.bind('<KeyPress>', self.key_pressed)
        self.pack()
        self.focus_set()
        self.set_framerate(50)
        # Init
        self.bird = Bird(self, self._bird_offset, self.height / 2)
        self.pipes = []
        self.pipes.append(Pipe(self))

    def set_framerate(self, rate):
        self._framerate = int(1000 / rate)

    def start(self):
        print('Starting...')
        self._running = True
        self.loop()

    def stop(self):
        print('Stopped !')
        self._running = False

    def loop(self):
        self.update()
        if self._running:
            self.after(self._framerate, self.loop)

    def key_pressed(self, event):
        if event.char == 'q':
            self._root_app.quit()
            return
        if event.char == 's':
            if self._running:
                self.stop()
            else:
                self.start()
            return
        if event.char == ' ':
            self.bird.up()
            return

    def update(self):
        self.frame_count += 1

        for pipe in self.pipes:
            pipe.update()
            pipe.draw()

        # if self.pipes[0].x + self.pipes[0].width > self._bird_offset:
        #     self.pipes[0].set_active()
        # else:
        #     self.pipes[1].set_active()
        pipe_info = self._get_next_pipe_info()
        self.bird.guess(pipe_info)

        self.bird.update()
        self.bird.draw()

        for i, pipe in enumerate(self.pipes):
            if pipe.hits(self.bird):
                print('HIT (%s)' % i)
                self.bird.hit()
                self.bird.fitness = self.frame_count
                self.stop()
                print('Your score : %s' % self.frame_count)

        self.pipes = [pipe for pipe in self.pipes if not pipe.off_screen()]

        if self.frame_count % 150 == 0:
            self.pipes.append(Pipe(self))

    def _get_next_pipe_info(self):
        next_pipe = None
        if self.pipes[0].x + self.pipes[0].width > self._bird_offset:
            next_pipe = self.pipes[0]
        else:
            next_pipe = self.pipes[1]
        next_pipe.set_active()
        dist = (next_pipe.x + next_pipe.width - self._bird_offset) / self.width
        h_top = next_pipe.get_htop() / self.height
        h_botton = next_pipe.get_hbottom() / self.height
        return [dist, h_top, h_botton]


#
# Main
#
if __name__ == '__main__':

    print('Flappy bird !')
    print('Python v%s' % platform.python_version())

    ROOT = Tk()
    APP = FlappyBirdApp(ROOT, 400, 400)
    ROOT.mainloop()
