from utils.layers import *
import tensorflow as tf

sq1x1 = "squeeze1x1"
exp1x1 = "expand1x1"
exp3x3 = "expand3x3"


def get_weights(weights, weight_name, bias_name):
    w = tf.constant(weights[weight_name], dtype=tf.float32)
    b = tf.constant(weights[bias_name], dtype=tf.float32)
    return w, b


def fire_module(x, weights, fire_id):
    s_id = 'fire' + str(fire_id) + '/'

    w, b = get_weights(weights, s_id + sq1x1 + '_W:0', s_id + sq1x1 + '_b:0')
    x = conv_2d(x, w, b, strides=1, padding='VALID', activation='relu')

    w, b = get_weights(weights, s_id + exp1x1 + '_W:0', s_id + exp1x1 + '_b:0')
    left = conv_2d(x, w, b, strides=1, padding='VALID', activation='relu')

    w, b = get_weights(weights, s_id + exp3x3 + '_W:0', s_id + exp3x3 + '_b:0')
    right = conv_2d(x, w, b, strides=1, padding='SAME', activation='relu')

    x = tf.concat([left, right], axis=3)
    return x


def SqueezeNet(x, weights):
    x = tf.reshape(x, shape=[-1, 227, 227, 3])

    w, b = get_weights(weights, 'conv1_W:0', 'conv1_b:0')
    x = conv_2d(x, w, b, strides=2, padding='VALID', activation='relu')
    x = maxpool_2d(x, k=3, s=2)

    x = fire_module(x, weights, fire_id=2)
    x = fire_module(x, weights, fire_id=3)
    x = maxpool_2d(x, k=3, s=2)

    x = fire_module(x, weights, fire_id=4)
    x = fire_module(x, weights, fire_id=5)
    x = maxpool_2d(x, k=3, s=2)

    x = fire_module(x, weights, fire_id=6)
    x = fire_module(x, weights, fire_id=7)
    x = fire_module(x, weights, fire_id=8)
    x = fire_module(x, weights, fire_id=9)

    w, b = get_weights(weights, 'conv10_W:0', 'conv10_b:0')
    x = conv_2d(x, w, b, strides=1, padding='VALID', activation='relu')

    x = avgpool_2d(x, k=7)
    x = tf.reshape(x, shape=[-1, 1000])
    return x


