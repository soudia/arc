import numpy as np
from sklearn import svm
from sklearn import ensemble
from sklearn import calibration
import copy

from arc import models

class Oracle:
    def __init__(self, model):
        self.model = model
    
    def fit(self,X,y):
        return self

    def predict(self, X):
        return model.sample(X)        

    def predict_proba(self, X):
        if(len(X.shape)==1):
            X = X.reshape((1,X.shape[0]))
        prob = self.model.compute_prob(X)
        prob = np.clip(prob, 1e-6, 1.0)
        prob = prob / prob.sum(axis=1)[:,None]
        return prob

class SVC:
    def __init__(self, calibrate=False, kernel = 'linear', C = 1, random_state = 2020):
        self.model = svm.SVC(kernel = kernel, C = C, probability = True, random_state = random_state)
        self.calibrate = calibrate
        
    def fit(self, X, y):
        self.model_fit = self.model.fit(X, y)
        if self.calibrate:
            self.calibrated = calibration.CalibratedClassifierCV(self.model_fit, method='sigmoid', cv=10)
        else:
            self.calibrated = None
        return copy.deepcopy(self)

    def predict(self, X):
        return self.model_fit.predict(X)

    def predict_proba(self, X):        
        if(len(X.shape)==1):
            X = X.reshape((1,X.shape[0]))
        if self.calibrated is None:
            prob = self.model_fit.predict_proba(X)
        else:
            prob = self.calibrated.predict_proba(X)
        prob = np.clip(prob, 1e-6, 1.0)
        prob = prob / prob.sum(axis=1)[:,None]
        return prob

class RFC:
    def __init__(self, calibrate=False, n_estimators = 1000, criterion="gini", 
                 max_depth=None, max_features="auto", random_state = 2020):
        self.model = ensemble.RandomForestClassifier(n_estimators=n_estimators, criterion=criterion,
                                                     max_depth=max_depth, max_features=max_features,
                                                     random_state = random_state)
        self.calibrate = calibrate
        
    def fit(self, X, y):
        self.model_fit = self.model.fit(X, y)
        if self.calibrate:
            self.calibrated = calibration.CalibratedClassifierCV(self.model_fit, method='sigmoid', cv=10)
        else:
            self.calibrated = None
        return copy.deepcopy(self)

    def predict(self, X):
        return self.model_fit.predict(X)

    def predict_proba(self, X):        
        if(len(X.shape)==1):
            X = X.reshape((1,X.shape[0]))
        if self.calibrated is None:
            prob = self.model_fit.predict_proba(X)
        else:
            prob = self.calibrated.predict_proba(X)
        prob = np.clip(prob, 1e-6, 1.0)
        prob = prob / prob.sum(axis=1)[:,None]
        return prob
