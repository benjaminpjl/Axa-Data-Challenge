import numpy as np

def linex(y_true, y_pred):
    alpha = -0.1
    grad = (-alpha*np.exp(alpha*(y_true-y_pred)) + alpha)
    hess = alpha*alpha*np.exp(alpha*(y_true-y_pred))

    return grad, hess

def evalerror_linex(y_true, y_pred):
     alpha = -0.1
     return 'error', np.mean(np.exp(alpha*(y_true-y_pred)) - alpha*(y_true-y_pred) - 1)
