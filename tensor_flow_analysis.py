import tensorflow as tf
import numpy as np
import os

substring_length = 5

correct_filename = "./meta/correct_substring_len_" + str(substring_length) + ".txt"
incorrect_filename = "./meta/incorrect_substring_len_" + str(substring_length) + ".txt"
variables_filename = "./meta/linear_regression_len_" + str(substring_length) + ".ckpt"
correct_list = []
incorrect_list = []
none_correct = 0
none_incorrect = 0



with file(correct_filename, "r") as f:
    for line in f:
        m = line.rsplit(' ', 1)
        if m[1]:
            if m[1] != "None\n":
                correct_list.append(float(m[1]))
            else:
                none_correct += 1

with file(incorrect_filename, "r") as f:
    for line in f:
        m = line.rsplit(' ', 1)
        if m[1]:
            if m[1] != "None\n":
                incorrect_list.append(float(m[1]))
            else:
                none_incorrect += 1

#print (len(correct_list))
#print (len(incorrect_list))
#print none_correct, none_incorrect

x_list = []
x_list.extend(correct_list)
x_list.extend(incorrect_list)
y_list = []
y_list.extend([1]*len(correct_list))
y_list.extend([0]*len(incorrect_list))

#print len (x_list), len (y_list)

# Create 100 phony x, y data points in NumPy, y = x * 0.1 + 0.3
#x_data = np.random.rand(100).astype(np.float32)
x_data = np.array(x_list)
y_data = np.array(y_list)


#print x_data[:100]
#print np.square(x_data[:100])

#print y_data[:100]
#print (len(x_data))

W = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
W2 = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
W3 = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
b = tf.Variable(tf.zeros([1]))
l = W3 * np.power(x_data,3)
k = W2 * np.square(x_data)
z = W * x_data

y = tf.add_n([l,z,k]) + b

# Minimize the mean squared errors.
loss = tf.reduce_mean(tf.square(y - y_data))
optimizer = tf.train.GradientDescentOptimizer(0.1)
train = optimizer.minimize(loss)

# Before starting, initialize the variables.  We will 'run' this first.
init = tf.initialize_all_variables()
saver = tf.train.Saver()
# Launch the graph.
sess = tf.Session()
sess.run(init)

if os.path.isfile(variables_filename):
    try:
        saver.restore(sess, variables_filename)
        print("Model restored.")
    except:
        pass

# Fit the line.
for step in range(20001):
    sess.run(train)

weight = sess.run(W)
weight2 = sess.run(W2)
weight3 = sess.run(W3)
bias = sess.run(b)


print "x3: %f x2: %f x: %f b: %f" % (weight3, weight2, weight, bias)
print "When no other options found: confidence interval %.2f%%" % (100*float(none_correct)/float(none_correct+none_incorrect))
for i in [x / 100.0 for x in range(0, 101, 4)]:
    print "When confidence interval %.2f - odds of success %.2f%%" % (i,100*((weight3*i*i*i)+(weight2*i*i)+(weight*i)+bias))

save_path = saver.save(sess, variables_filename)