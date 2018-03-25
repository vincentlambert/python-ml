import sys
sys.path.append('./src/neural_network')

from tkinter import *
import platform

from bird import *
from pipe import *

POPULATION_SIZE = 100

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
        self.bind('<KeyPress>', self.key_pressed)
        self.pack()
        self.focus_set()
        self.set_framerate(50)
        self.best_distance = 0
        self.generation_count = 1
        # Init
        self.frame_count = 0
        self.birds = []
        self.pipes = []
        self.init()

    def set_framerate(self, rate):
        self._framerate = int(1000 / rate)

    def init(self, evolve=False):
        new_population = []
        # Calculate next generation
        if evolve:
            birds_fitness = [bird.fitness for bird in self.birds]
            for _ in range(len(self.birds)):
                parent_a = random.choices(self.birds, weights=birds_fitness).pop()
                parent_b = random.choices(self.birds, weights=birds_fitness).pop()
                new_population.append(Bird(self, self._bird_offset, self.height / 2, parent_a=parent_a, parent_b=parent_b))

        # Destroy obsolete objects
        for bird in self.birds:
            bird.destroy()
        for pipe in self.pipes:
            pipe.destroy()
        self.frame_count = 0
        self.pipes = []

        # Init next generation
        if evolve:
            self.birds = new_population
            self.generation_count += 1           
        else:
            self.generation_count = 1
            self.birds = []
            for _ in range(POPULATION_SIZE):
                self.birds.append(Bird(self, self._bird_offset, self.height / 2))

    def start(self):
        self._running = True
        self.loop()

    def stop(self):
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
                print('Stopped !')
            else:
                print('Starting...')
                self.start()
            return
        if event.char == 'r':
            self.init()
            self.start()
            print('Restarted...')
            return
        if event.char == 'l':
            for i, bird in enumerate(self.birds):
                print('%s\t%s' % (i,bird))
            return
        if event.char == 'i':
            print('Generation : %s' % self.generation_count)
            print('Best fitness : %s' % self.best_distance)
            return

        # if event.char == ' ':
        #     self.bird.up()
        #     return

    def update(self):
        # Create new pipe
        if self.frame_count % 150 == 0:
            self.pipes.append(Pipe(self))
        self.frame_count += 1
        # print('FRAME %s' % self.frame_count)

        # Update pipe
        for pipe in self.pipes:
            pipe.update()
            pipe.draw()

        # Get next pipe info
        dist, h_top, h_botton = self._get_next_pipe_info()

        # Update birds
        for bird in self.birds:
            bird.guess(dist, h_top, h_botton)
            bird.update(self.frame_count)
            bird.draw()

        # Check bird hit
        for pipe in self.pipes:
            for bird in self.birds:
                if not bird.is_hit():
                    if(pipe.hits(bird)):
                        bird.hit(self.frame_count)

        # Delete off screen pipes
        [pipe.destroy() for pipe in self.pipes if pipe.off_screen()]
        self.pipes = [pipe for pipe in self.pipes if not pipe.off_screen()]

        # Calc best fitness
        if not [bird for bird in self.birds if not bird.is_hit()]:
            best = max([bird.fitness for bird in self.birds])
            if best > self.best_distance:
                self.best_distance = best
            print('Max fitness / best fitness : %s/%s' % (best, self.best_distance))
            #self.stop()
            self.init(evolve=True)
            #self.start()

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
        return dist, h_top, h_botton


#
# Main
#
if __name__ == '__main__':

    print('Flappy bird !')
    print('Python v%s' % platform.python_version())

    ROOT = Tk()
    APP = FlappyBirdApp(ROOT, 400, 400)
    #APP.set_framerate(5)
    ROOT.mainloop()
