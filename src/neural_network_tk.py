#
# Draw neural network heatmap with Tkinter
#
from neural_network import *
from tkinter import *

class MyApp(Canvas):
    def __init__(self, root, width, height):
        Canvas.__init__(self, root, width=width, height=height)
        self._root_app = root
        self.bind('<KeyPress>', self.key_pressed)
        self.pack()
        self.focus_set()
        self.set_framerate(50)
        self._running = False
    
    def set_framerate(self, rate):
        self._framerate = int(1000 / rate)

    def start(self):
        self._running = True
        self.loop()

    def stop(self):
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
    
    def init(self):
        pass

    def update(self):
        print('update')
        pass


#
# Main
#
if __name__ == '__main__':
    print("*****")
    print("***** Main...")
    print("*****")

    # Neural network training for XOR
    nn = NeuralNetwork(2, 3, 1)
    # print('***** Before training')
    # testNN(nn)
    # trainNN(nn, 100000)
    # print('***** After training')
    # testNN(nn)

    # Plot heatmap
    root = Tk()
    app = MyApp(root, 400, 400)
    app.set_framerate(10)
    app.init()
    root.mainloop()
