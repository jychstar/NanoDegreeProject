# code based on official tensorflow tutorial: expert
# to cite graph in javascript or markdown, <img src="" alt="Smiley face" width="600">

import tensorflow as tf

x = tf.placeholder(tf.float32, shape=[None, 784], name = "input")
y_ = tf.placeholder(tf.float32, shape=[None, 10], name = "label")   # labels

# Weight Initialization
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial, name = "weight")

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial, name = "bias")

# Convolution and Pooling
def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME', name = "conv2d")

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME', name="max_pool")

with tf.name_scope("Convolutional_1"):
    x_image = tf.reshape(x, [-1,28,28,1])
    W_conv1 = weight_variable([5, 5, 1, 32]) # 2D patch sizes, input/output channels
    b_conv1 = bias_variable([32])
    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1, name="relu")
    h_pool1 = max_pool_2x2(h_conv1)

with tf.name_scope("Convolutional_2"):
    W_conv2 = weight_variable([5, 5, 32, 64])
    b_conv2 = bias_variable([64])

    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2, name="relu")
    h_pool2 = max_pool_2x2(h_conv2)
with tf.name_scope("Densely"):
    W_fc1 = weight_variable([7 * 7 * 64, 1024])
    b_fc1 = bias_variable([1024])
    h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1, name="relu")

# Dropout
keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob, name = "dropout")

with tf.name_scope("Readout"):
    W_fc2 = weight_variable([1024, 10])
    b_fc2 = bias_variable([10])
    y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
with tf.name_scope("softmax"):
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y_conv, labels=y_))
with tf.name_scope("train"):
    train_step = tf.train.AdamOptimizer(1e-4).minimize(loss)  # more sophisticated ADAM optimizer
with tf.name_scope("accuracy"):
    correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

feed_test = {x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0} 

# execute phase ==========================================================
folder = 'board_expert'
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    writer = tf.summary.FileWriter(folder)  # create writer
    writer.add_graph(sess.graph)
    print("graph is written into folder:", folder)