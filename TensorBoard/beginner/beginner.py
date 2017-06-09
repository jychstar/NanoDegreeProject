import argparse
import sys

from tensorflow.examples.tutorials.mnist import input_data
from time import time
t0 = time()

import tensorflow as tf

tf.summary.FileWriterCache.clear()
# Import data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True) # object, not data

# construction phase
X = tf.placeholder(tf.float32, [None, 784], name = "input_1")
x_image = tf.summary.image('input', tf.reshape(X, [-1, 28, 28, 1]), 3)

y_ = tf.placeholder(tf.float32, [None, 10], name = "label")

with tf.name_scope("hidden"):
    W = tf.Variable(tf.zeros([784, 10]),name = "Weight")
    b = tf.Variable(tf.zeros([10]),name = "Bias")
    y = tf.matmul(X, W) + b
    # tf.summary.histogram("weights",W)
    # tf.summary.histogram("bias",b)
    y_historgram = tf.summary.histogram("activation",y)
with tf.name_scope("softmax"):
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y), name ="softmax_cross_entropy")
with tf.name_scope("train"):
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(loss)
with tf.name_scope("accuracy"):
    # Test trained model
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    accuracy_scalar = tf.summary.scalar("accuracy",accuracy)

#merge = tf.summary.merge_all()    
saver = tf.train.Saver()

# execute phase
sess = tf.InteractiveSession()
# saver.restore(sess, "/tmp/model.ckpt")
tf.global_variables_initializer().run()

# tf.summary.FileWriter('board_beginner',sess.graph)   # magic board  
writer = tf.summary.FileWriter('board_beginner')  # create writer
writer.add_graph(sess.graph)

feed_test = {X: mnist.test.images,y_: mnist.test.labels}
# Train
batch_size =100
step_num = 1001
for step in range(step_num):
    batch_xs, batch_ys = mnist.train.next_batch(batch_size) # origianl 100
    feed_train = {X: batch_xs, y_: batch_ys}
    sess.run(train_step, feed_dict = feed_train)
    
    if step % 20 == 0:
        sum1 = sess.run(x_image, feed_dict=feed_train)
        sum2 = sess.run(accuracy_scalar, feed_dict=feed_train)
        sum3 = sess.run(y_historgram, feed_dict=feed_train)
        writer.add_summary(sum1,step)
        writer.add_summary(sum2,step)
        writer.add_summary(sum3,step)
    
    if step % 200 == 0:
        print('interation={0:4},loss={1:4}'.format(step,sess.run(loss,feed_dict=feed_test)))
saver.save(sess, "model_beginner")
            
print("test accuracy {0:g}".format(accuracy.eval(feed_dict=feed_test)))
print("time cost:",time()-t0) # get 0.92 in 230 seconds; 