import sys

_, model_path, niter = sys.argv

niter = int(niter)

from pylearn2.utils import serial

model = serial.load(model_path)

import theano.tensor as T

X = T.matrix()

Y_hat = model.inference_procedure.multi_infer(X, niter=niter)

Y = T.matrix()

y_hat = T.argmax(Y_hat, axis=1)
y = T.argmax(Y, axis=1)

misclass = T.neq(y_hat, y).mean()

from theano import function
f = function([X, Y], misclass)

from pylearn2.datasets.mnist import MNIST

dataset = MNIST(which_set='test', one_hot=1)

print f(dataset.X, dataset.y)
