#
# Maze solving
#
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

def draw_maze(image):
    width = image.size[0]
    height = image.size[1]
    print('Maze size : %s x %s' % (width, height))
    for cur_y in range(0, height):
        line = ''
        for cur_x in range(0, width):
            if image.getpixel((cur_x, cur_y)) == 0:
                line = line + 'X'
            else:
                line = line + ' '
        print(line)

def main():
    print('Main started...')
    image = Image.open('./data/maze_sample/tiny.png')
    print('Image loaded')
    draw_maze(image)
    print('Done')

if __name__ == '__main__':
    main()
