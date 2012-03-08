from sklearn.linear_model import LogisticRegression
import numpy as np

class HackyMulticlassLogistic:

    """ A hacky version of the multiclass logistic
        This is intentionally hacky, ie the code is not hacky, the math is
        Rather than doing a softmax, we fit each logistic on its own, then
        just report the max during classification.
        This is what Jia+Huang used to get state of the art on CIFAR-100
    """

    def __init__(self, C):
        self.C = C

    def fit(self, X,y):

        min_y = y.min()
        max_y = y.max()

        assert min_y == 0

        num_classes = max_y + 1
        assert num_classes > 1

        logistics = []

        for c in xrange(num_classes):

            print 'fitting class ',c
            cur_y = (y == c).astype('int32')

            logistics.append(LogisticRegression(C = self.C).fit(X,cur_y))

        return Classifier(logistics)

class Classifier:
    def __init__(self, logistics):
        assert len(logistics) > 1

        num_classes = len(logistics)
        num_features = logistics[0].coef_.shape[1]

        self.W = np.zeros((num_features, num_classes))
        self.b = np.zeros((num_classes,))

        for i in xrange(num_classes):
            self.W[:,i] = logistics[i].coef_
            self.b[i] = logistics[i].intercept_

    def predict(self, X):

        return np.argmax(self.b + np.dot(X,self.W), 1)


