#
# Tensorflow tests
#
#import numpy as np
import tensorflow as tf

def simple_test():
    c1 = tf.constant([1, 2, 3], shape=[1, 3])
    c2 = tf.constant([1, 2, 3], shape=[3, 1])
    res = c1 @ c2 # Equ to tf.matmul(c1, c2)
    print(c1)

    session = tf.Session()
    #session.run(tf.global_variables_initializer())
    print(session.run(c1))
    print(session.run(c2))
    print(session.run(res))

if __name__ == '__main__':
    simple_test()
