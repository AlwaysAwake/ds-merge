import tensorflow as tf
import json


#Data
with open('training_set.json') as infile:
    data = json.load(infile)
    data_x = list()
    data_y = list()
    for year in range(2007,2016):
        for match in data[str(year)]:
            data_x.append(match[0:1078])
            data_y.append(match[1078:1081])
    for key, value in enumerate(data_x):
        for k, v in enumerate(value):
            data_x[key][k] = float(v)/100
    test_x = list()
    test_y = list()
    for match in data['2016']:
        test_x.append(match[0:1078])
        test_y.append(match[1078:1081])
    for key, value in enumerate(test_x):
        for k, v in enumerate(value):
            test_x[key][k] = float(v)/100

def get_batch(i, batch_size, data_x, data_y):
    x_batch = data_x[int(i*batch_size):int((i+1)*batch_size)]
    y_batch = data_y[int(i*batch_size):int((i+1)*batch_size)] 
    return (x_batch, y_batch)

# Parameters
learning_rate = 0.001
training_epochs = 10
batch_size = 10
display_step = 1

# Network Parameters
n_hidden = 1078
n_input = 1078
n_classes = 3 

# tf Graph input
x = tf.placeholder("float", [None, n_input])
y = tf.placeholder("float", [None, n_classes])
result = tf.placeholder("float", [None, n_classes])
# Create model
def multilayer_perceptron(x, weights, biases, layers):

    layer = {}
    for i in range(layers):
        if i is 0:
            layer[i+1] = tf.add(tf.matmul(x, weights['h'+str(i+1)]), biases['b'+str(i+1)])
            layer[i+1] = tf.nn.relu(layer[i+1])
        else:
            layer[i+1] = tf.add(tf.matmul(layer[i], weights['h'+str(i+1)]), biases['b'+str(i+1)])
            layer[i+1] = tf.nn.relu(layer[i+1])
    
    out_layer = tf.matmul(layer[layers], weights['out']) + biases['out']
    return out_layer

# Store layers weight & bias
weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden])),
    'h2': tf.Variable(tf.random_normal([n_hidden, n_hidden])),
    'h3': tf.Variable(tf.random_normal([n_hidden, n_hidden])),
    'h4': tf.Variable(tf.random_normal([n_hidden, n_hidden])),
    'h5': tf.Variable(tf.random_normal([n_hidden, n_hidden])),
    'h6': tf.Variable(tf.random_normal([n_hidden, n_hidden])),
    'h7': tf.Variable(tf.random_normal([n_hidden, n_hidden])),
    'h8': tf.Variable(tf.random_normal([n_hidden, n_hidden])),
    'h9': tf.Variable(tf.random_normal([n_hidden, n_hidden])),
    'h10': tf.Variable(tf.random_normal([n_hidden, n_hidden])),
    'h11': tf.Variable(tf.random_normal([n_hidden, n_hidden])),
    'h12': tf.Variable(tf.random_normal([n_hidden, n_hidden])),
    'h13': tf.Variable(tf.random_normal([n_hidden, n_hidden])),
    'h14': tf.Variable(tf.random_normal([n_hidden, n_hidden])),
    'h15': tf.Variable(tf.random_normal([n_hidden, n_hidden])),
    'out': tf.Variable(tf.random_normal([n_hidden, n_classes]))
}
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden])),
    'b2': tf.Variable(tf.random_normal([n_hidden])),
    'b3': tf.Variable(tf.random_normal([n_hidden])),
    'b4': tf.Variable(tf.random_normal([n_hidden])),
    'b5': tf.Variable(tf.random_normal([n_hidden])),
    'b6': tf.Variable(tf.random_normal([n_hidden])),
    'b7': tf.Variable(tf.random_normal([n_hidden])),
    'b8': tf.Variable(tf.random_normal([n_hidden])),
    'b9': tf.Variable(tf.random_normal([n_hidden])),
    'b10': tf.Variable(tf.random_normal([n_hidden])),
    'b11': tf.Variable(tf.random_normal([n_hidden])),
    'b12': tf.Variable(tf.random_normal([n_hidden])),
    'b13': tf.Variable(tf.random_normal([n_hidden])),
    'b14': tf.Variable(tf.random_normal([n_hidden])),
    'b15': tf.Variable(tf.random_normal([n_hidden])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}

max_accuracy = 0.0
max_layer = 0
accuracy_dict = {}
for i in range(5, 8):
    # Construct model
    pred = multilayer_perceptron(x, weights, biases, i)

    # Define loss and optimizer
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(pred,y))
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

    # Initializing the variables
    init = tf.initialize_all_variables()
    saver = tf.train.Saver()
    # Launch the graph
    with tf.Session() as sess:
        sess.run(init)

        # Training cycle
        for epoch in range(training_epochs):
            avg_cost = 0.
            total_batch = int(len(data_x[0:int(len(data_x)*0.8)])/batch_size)
            # Loop over all batches
            for j in range(total_batch):
                batch_x, batch_y = get_batch(j, batch_size, data_x[0:int(len(data_x)*0.8)], data_y[0:int(len(data_y)*0.8)])
                # Run optimization op (backprop) and cost op (to get loss value)
                _, c = sess.run([optimizer, cost], feed_dict={x: batch_x,
                                                              y: batch_y})
                
                # Compute average loss
                avg_cost += c / total_batch
            # Display logs per epoch step
            if epoch % display_step == 0:
                print "Epoch:", '%04d' % (epoch+1), "cost=", \
                    "{:.9f}".format(avg_cost)
        print "Optimization Finished!"
        saver.save(sess, 'layer.ckpt', global_step = i) 
        # Test model
        correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
        # Calculate accuracy
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
       
        # CV
        acc_result = accuracy.eval({x: data_x[int(len(data_x)*0.8):], y: data_y[int(len(data_y)*0.8):]})
        if acc_result > max_accuracy:
            max_accuracy = acc_result
            max_layer = i
        print "Accuracy:", acc_result
        accuracy_dict[i] = acc_result
        
        with open('accuracy_result.json','w') as outfile:
            save_data = {}
            for k,v in accuracy_dict.iteritems():
                save_data[str(k)] = str(v)
            json.dump(save_data, outfile) 

for key, value in accuracy_dict.iteritems():
    print "# of layer: %s / accuracy: %s" % (key, value)
print "most accurate layer : %s" % max_layer
#-----------------------After Learning-----------------------------#
pred = multilayer_perceptron(x, weights, biases, max_layer)

# Define loss and optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(pred, y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

# Initializing the variables
init = tf.initialize_all_variables()
saver = tf.train.Saver()
with tf.Session() as sess:
    sess.run(init)
    saver = tf.train.import_meta_graph('layer.ckpt-'+str(max_layer)+'.meta')
    saver.restore(sess, 'layer.ckpt-'+str(max_layer))
    
    correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    predicted = sess.run(tf.argmax(pred,1), feed_dict={x: test_x, y:test_y})
  
    total_count = 0
    correct_count = 0
    result_data = {}

    for key, value in enumerate(predicted):
        match_result = -1
        for k, v in enumerate(test_y[key]):
            if v > 0: match_result = k
        result_comp = {}
        result_comp['prediction'] = str(value)
        result_comp['real match'] = str(match_result)
        result_data[str(key)] = result_comp
        print "predicted: %s / match_result: %s" % (value, match_result)
        total_count += 1 
        if match_result == value:
            correct_count += 1
    print "%s / %s" % (correct_count , total_count)

    with open('predict_result.json', 'w') as outfile:
        json.dump(result_data, outfile)

    # Calculate accuracy
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    print "Accuracy:", accuracy.eval({x: test_x, y: test_y}) 
