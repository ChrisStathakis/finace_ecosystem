import tensorflow as tf

import hy_param


X = tf.placeholder("float", [None, hy_param.num_input], name="input_x")