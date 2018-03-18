#
# Draw neural network heatmap with Matplotlib
#
from neural_network import *
import matplotlib.pyplot as plt

def draw_heatmap(neural_network):
    step = 10
    data = []
    labels = []

    for i in range(0, step + 1):
        labels.append(i / step)

    for x1 in range(0, step + 1):
        data.append([])
        for x2 in range(0, step + 1):
            data[x1].append(neural_network.predict([x1 / step, x2 / step]).item())

    # Mode 1
    # fig, axis = plt.subplots()
    # heatmap = axis.pcolor(data, cmap=plt.cm.Greys)
    # axis.set_title('Network response')
    # print(repr(fig))
    # print(repr(axis))

    # Mode 2
    x, y = np.meshgrid(labels, labels)
    intensity = np.array(data)
    plt.pcolormesh(x, y, intensity, cmap=plt.cm.YlOrRd)
    plt.colorbar()
    plt.show()

#
# Main
#
if __name__ == '__main__':
    print("*****")
    print("***** Main...")
    print("*****")

    # Neural network training for XOR
    nn = NeuralNetwork(2, 3, 1)
    print('***** Before training')
    testNN(nn)
    trainNN(nn, 100000)
    print('***** After training')
    testNN(nn)

    # Plot heatmap
    draw_heatmap(nn)
