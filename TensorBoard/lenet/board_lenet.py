import tensorflow as tf
mu = 0
sigma = 0.1
rate = 0.001

x = tf.placeholder(tf.float32, (None, 32, 32, 1), name = "input")
y = tf.placeholder(tf.int32, (None),name = "label")
one_hot_y = tf.one_hot(y, 10)

with tf.name_scope("conv1"):   # Layer 1: Convolutional. Input = 32x32x1. Output = 28x28x6.
    conv1_W = tf.Variable(tf.truncated_normal(shape=(5, 5, 1, 6), mean = mu, stddev = sigma),name = "weight")
    conv1_b = tf.Variable(tf.zeros(6),name = "bias")
    conv1   = tf.nn.conv2d(x, conv1_W, strides=[1, 1, 1, 1], padding='VALID') + conv1_b
    relu1 = tf.nn.relu(conv1, name = "relu1")
    # SOLUTION: Pooling. Input = 28x28x6. Output = 14x14x6.
    pool1 = tf.nn.max_pool(relu1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='VALID', name = "max_pool")

with tf.name_scope("conv2"):     # SOLUTION: Layer 2: Convolutional. Output = 10x10x16.
    conv2_W = tf.Variable(tf.truncated_normal(shape=(5, 5, 6, 16), mean = mu, stddev = sigma),name = "weight")
    conv2_b = tf.Variable(tf.zeros(16),name = "bias")
    conv2   = tf.nn.conv2d(pool1, conv2_W, strides=[1, 1, 1, 1], padding='VALID') + conv2_b
    relu2 = tf.nn.relu(conv2, name = "relu2")
    # SOLUTION: Pooling. Input = 10x10x16. Output = 5x5x16.
    pool2 = tf.nn.max_pool(conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='VALID', name = "max_pool")
    # SOLUTION: Flatten. Input = 5x5x16. Output = 400.
    fc0   = tf.contrib.layers.flatten(pool2)
    
with tf.name_scope("dense1"):    # SOLUTION: Layer 3: Fully Connected. Input = 400. Output = 120.
    fc1_W = tf.Variable(tf.truncated_normal(shape=(400, 120), mean = mu, stddev = sigma),name = "weight")
    fc1_b = tf.Variable(tf.zeros(120),name = "bias")
    fc1    = tf.nn.relu(tf.matmul(fc0, fc1_W) + fc1_b, name = "relu")

with tf.name_scope("dense2"):     # SOLUTION: Layer 4: Fully Connected. Input = 120. Output = 84.
    fc2_W  = tf.Variable(tf.truncated_normal(shape=(120, 84), mean = mu, stddev = sigma),name = "weight")
    fc2_b  = tf.Variable(tf.zeros(84),name = "bias")
    fc2    = tf.nn.relu(tf.matmul(fc1, fc2_W) + fc2_b, name = "relu")

with tf.name_scope("dense3"):     # SOLUTION: Layer 5: Fully Connected. Input = 84. Output = 10.
    fc3_W  = tf.Variable(tf.truncated_normal(shape=(84, 10), mean = mu, stddev = sigma),name = "weight")
    fc3_b  = tf.Variable(tf.zeros(10),name = "bias")
    logits = tf.matmul(fc2, fc3_W) + fc3_b
    
with tf.name_scope("softmax"): 
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=one_hot_y)
    loss_operation = tf.reduce_mean(cross_entropy)
with tf.name_scope("train"):
    optimizer = tf.train.AdamOptimizer(learning_rate = rate)
    training_operation = optimizer.minimize(loss_operation)    
with tf.name_scope("accuracy"):
    correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(one_hot_y, 1))
    accuracy_operation = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
# execute phase ==========================================================
folder = 'board_lenet'
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    writer = tf.summary.FileWriter(folder)  # create writer
    writer.add_graph(sess.graph)
    print("graph is written into folder:", folder)