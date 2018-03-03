from tkinter import *
from perceptron import *

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400

class MyApp(Canvas):
    def __init__(self, root, width, height):
        Canvas.__init__(self, root, width=width, height=height)
        self.bind('<KeyPress>', self.keyPressed)
        self.pack()
        self.focus_set()
        self.setFrameRate(50)
        self.running = False
    
    def setFrameRate(self, rate):
        self.frame_rate = int(1000 / rate)
        self.frame_rate += 0
    
    def start(self):
        self.running = True
        self.loop()
    
    def stop(self):
        self.running = False
    
    def loop(self):
        self.update()
        if self.running:
            self.after(self.frame_rate, self.loop)

    def init(self):
        self.create_line(translateX(-1), translateY(f(-1)), translateX(1), translateY(f(1)), fill='#000000')
        self.perceptron = Perceptron(100, self)
        self.guess_line = self.create_line(translateX(-1),
                                          translateY(self.perceptron.guessY(-1)),
                                          translateX(1),
                                          translateY(self.perceptron.guessY(1)),
                                          fill='#FF0000')

    def update(self):
        self.perceptron.learn()
        self.perceptron.draw()
        self.coords(self.guess_line,
                    translateX(-1),
                    translateY(self.perceptron.guessY(-1)),
                    translateX(1),
                    translateY(self.perceptron.guessY(1)))

    def keyPressed(self, e):
        if e.char == 'q':
            root.quit()
            return
        if e.char =='s':
            if self.running:
                self.stop()
            else:
                self.start()

print('Running perceptron UI')
root = Tk()
app = MyApp(root, CANVAS_WIDTH, CANVAS_HEIGHT)
app.setFrameRate(10)
app.init()
#app.start()

root.mainloop()
