import tensorflow as tf
import numpy as np

substring_length = 5

correct_filename = "./meta/correct_substring_len_" + str(substring_length) + ".txt"
incorrect_filename = "./meta/incorrect_substring_len_" + str(substring_length) + ".txt"
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
#print y_data[:100]
#print (len(x_data))

# Try to find values for W and b that compute y_data = W * x_data + b
# (We know that W should be 0.1 and b 0.3, but TensorFlow will
# figure that out for us.)
W = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
b = tf.Variable(tf.zeros([1]))
y = W * x_data + b


# Minimize the mean squared errors.
loss = tf.reduce_mean(tf.square(y - y_data))
optimizer = tf.train.GradientDescentOptimizer(0.5)
train = optimizer.minimize(loss)

# Before starting, initialize the variables.  We will 'run' this first.
init = tf.initialize_all_variables()

# Launch the graph.
sess = tf.Session()
sess.run(init)

# Fit the line.
for step in range(2001):
    sess.run(train)

weight = sess.run(W)
bias = sess.run(b)

print "x: %f b: %f" % (weight,bias)
print "When no other options found: confidence interval %.2f%%" % (100*float(none_correct)/float(none_correct+none_incorrect))
#print "When confidence interval 0 - odds of success %f%%" % (100*bias)
for i in [x / 100.0 for x in range(1, 101, 6)]:
    print "When confidence interval %.2f - odds of success %.2f%%" % (i,100*((weight*i)+bias))

