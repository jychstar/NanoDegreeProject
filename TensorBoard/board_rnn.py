import tensorflow as tf
from tensorflow.contrib import seq2seq
vocab_size = 6779
rnn_size = 256

input_text = tf.placeholder(tf.int32, [None, None], name='input')
targets = tf.placeholder(tf.int32, [None, None], name='targets')
learingRate = tf.placeholder(tf.float32, name='learingRate')
input_data_shape = tf.shape(input_text)
with tf.name_scope("initial_rnn_cell"):
    lstm = tf.contrib.rnn.BasicLSTMCell(rnn_size)
    cell = tf.contrib.rnn.MultiRNNCell([lstm])
    initial_state = tf.identity (cell.zero_state (input_data_shape[0], tf.float32), name="initial_state")
with tf.name_scope("embed"): 
    embedding = tf.Variable(tf.random_uniform((vocab_size, rnn_size), -1, 1), name = "embedding")
    embed = tf.nn.embedding_lookup(embedding, input_text, name = "lookup")
#with tf.name_scope("build_rnn"):
outputs, final_state = tf.nn.dynamic_rnn(cell, embed ,dtype = tf.float32)
final_state = tf.identity(final_state, name = "final_state")
logits = tf.contrib.layers.fully_connected(outputs, vocab_size, activation_fn= None, name ="logits")

with tf.name_scope("softmax"):
    probs = tf.nn.softmax(logits, name='probs')
    cost = seq2seq.sequence_loss(logits,targets,tf.ones([input_data_shape[0], input_data_shape[1]]))
#with tf.name_scope("train"):
optimizer = tf.train.AdamOptimizer(learingRate)
gradients = optimizer.compute_gradients(cost)
capped_gradients = [(tf.clip_by_value(grad, -1., 1.), var) for grad, var in gradients]
train_op = optimizer.apply_gradients(capped_gradients)

folder = 'board_rnn'
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    writer = tf.summary.FileWriter(folder)  # create writer
    writer.add_graph(sess.graph)
    print("graph is written into folder:", folder)
    
# tensorboard --logdir "board_rnn"