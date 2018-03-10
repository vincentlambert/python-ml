#
# Draw neural network heatmap with Tkinter
#
from neural_network import *
from tkinter import *

class MyApp(Canvas):
    def __init__(self, root, width, height):
        Canvas.__init__(self, root, width=width, height=height)
        self._width = width
        self._height = height
        self._root_app = root
        self.bind('<KeyPress>', self.key_pressed)
        self.pack()
        self.focus_set()
        self.set_framerate(50)
        self._running = False
        self._step = 10
        self._neuralnetwork = NeuralNetwork(2, 3, 1)
        self._heatmap = []
    
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

    def key_pressed(self, e):
        if e.char == 'q':
            self._root_app.quit()
            return
        if e.char == 's':
            if self._running:
                self.stop()
            else:
                self.start()
            return
        if e.char == 't':
            self.test()
            return
        if e.char == 'r':
            self.reset()
            return
    
    def init(self):
        for x1 in range(0, self._step + 1):
            for x2 in range(0, self._step + 1):
                prediction = self._neuralnetwork.predict([x1 / self._step, x2 / self._step]).item()
                color = '#%02x%02x%02x' % (int(prediction * 255), int(prediction * 255), int(prediction * 255))
                self._heatmap.append(self.create_rectangle(x1 * self._width / (self._step + 1),
                                                           x2 * self._width / (self._step + 1),
                                                           (x1 + 1) * self._width / (self._step + 1),
                                                           (x2 + 1) * self._width / (self._step + 1),
                                                           fill=color))

    def update(self):
        trainNN(self._neuralnetwork, 1000)
        for x1 in range(0, self._step + 1):
            for x2 in range(0, self._step + 1):
                prediction = self._neuralnetwork.predict([x1 / self._step, x2 / self._step]).item()
                color = '#%02x%02x%02x' % (int(prediction * 255), int(prediction * 255), int(prediction * 255))
                self.itemconfig(self._heatmap[x2 + x1 * (self._step + 1)], fill=color)

    def test(self):
        print('Test')
        print('[1, 0] ==> %s' % self._neuralnetwork.predict([1, 0]))
        print('[0, 1] ==> %s' % self._neuralnetwork.predict([0, 1]))
        print('[1, 1] ==> %s' % self._neuralnetwork.predict([1, 1]))
        print('[0, 0] ==> %s' % self._neuralnetwork.predict([0, 0]))

    def reset(self):
        print('Reset')
        self._neuralnetwork = NeuralNetwork(2, 3, 1)


#
# Main
#
if __name__ == '__main__':
    print("*****")
    print("***** Main...")
    print("*****")

    # Plot heatmap
    root = Tk()
    app = MyApp(root, 400, 400)
    app.set_framerate(10)
    app.init()
    root.mainloop()
