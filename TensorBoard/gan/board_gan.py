import tensorflow as tf
tf.reset_default_graph()
inputs_z = tf.placeholder(tf.float32, (None, 100), name='input_z')
inputs_real = tf.placeholder(tf.float32, (None, 784), name='input_real') 

with tf.variable_scope('generator', reuse=False):        
    h1 = tf.layers.dense(inputs_z, 128, activation=None, name = "dense")  # Hidden layer        
    h1 = tf.maximum(0.01 * h1, h1)  # Leaky ReLU
    logits = tf.layers.dense(h1, 784, activation=None, name = "fake_image")  
    inputs_fake = tf.tanh(logits)    
    
with tf.variable_scope('discriminator', reuse=False):
    h1 = tf.layers.dense(inputs_real, 128, activation=None, name = "dense")
    h1 = tf.maximum(0.01 * h1, h1)
    d_logits_real = tf.layers.dense(h1, 1, activation=None, name = "logits")
    #d_model_real = tf.sigmoid(logits)

with tf.variable_scope('discriminator', reuse=True):
    h1 = tf.layers.dense(inputs_fake, 128, activation=None, name = "dense")
    h1 = tf.maximum(0.01 * h1, h1)
    d_logits_fake = tf.layers.dense(h1, 1, activation=None, name = "logits")
    #d_model_fake = tf.sigmoid(logits)    
with tf.name_scope("d_loss"):
    d_loss_real = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(
            logits=d_logits_real, labels=tf.ones_like(d_logits_real) * 0.9), name = "d_loss_real")
    d_loss_fake = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(
            logits=d_logits_fake, labels=tf.zeros_like(d_logits_real)), name = "d_loss_fake")
    d_loss = d_loss_real + d_loss_fake
with tf.name_scope("g_loss"):
    g_loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(
            logits=d_logits_fake,labels=tf.ones_like(d_logits_fake)), name = "generation_loss")
# Optimizers
learning_rate = 0.002
# Get the trainable_variables, split into G and D parts
t_vars = tf.trainable_variables()
g_vars = [var for var in t_vars if var.name.startswith('generator')]
d_vars = [var for var in t_vars if var.name.startswith('discriminator')]
with tf.name_scope("d_train"):
    d_train_opt = tf.train.AdamOptimizer(learning_rate).minimize(d_loss, var_list=d_vars)
with tf.name_scope("g_train"):    
    g_train_opt = tf.train.AdamOptimizer(learning_rate).minimize(g_loss, var_list=g_vars)    
# execute phase ==========================================================
folder = 'board_gan'
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    writer = tf.summary.FileWriter(folder)  # create writer
    writer.add_graph(sess.graph)
    print("graph is written into folder:", folder)    