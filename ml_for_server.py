import ast

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.svm import LinearSVC
from SVO import find_svo


class ml:
    def __init__(self, path=None):
        if(path):
            self.read_data(path)

    def j_score(self,y_true,y_pred):
        jaccard = np.minimum(y_true,y_pred).sum(axis=1)/np.maximum(y_true,y_pred).sum(axis=1)
        return jaccard.mean() * 100

    def read_data(self,path):
        self.df = pd.read_csv('./train_svo') # Will be changed to db connection
        self.df['Category'] = self.df['Category'].apply(lambda x: ast.literal_eval(x))
        self.multilabel = MultiLabelBinarizer()
        self.y = self.multilabel.fit_transform(self.df['Category'])
    
    def train(self):
        #print(self.multilabel.classes_)
        #a = pd.DataFrame(self.y,columns=self.multilabel.classes_)
        #print(self.df['Message'])
        self.tfidf = TfidfVectorizer(analyzer='word',max_features=1000) #we can play around with the max_features value
        self.X = self.tfidf.fit_transform(self.df['Message'])
        #print(self.tfidf.vocabulary_)
        #print(self.X.shape)
        #^prints number of rows and number of features per row. Our data is small (200 values), so we only have 195 features. 
        # For larger dataset, we can have up to 1000 features (or more depending on max_features value)
        #print(self.y.shape)
        #^prints number of rows (same as X.shape rows) and number of tags we assigned. In our case, there are only 6 tags.

        X_train, X_test, y_train, self.y_test = train_test_split(self.X,self.y,test_size=0.2,random_state=0,stratify=self.y)
        #^With test size = 0.2, we need to have at least 2 sentences per category. If there are less, we need to remove stratify=y

        sgd = SGDClassifier()
        lr = LogisticRegression(solver='lbfgs')
        svc=LinearSVC()
        for classifier in [sgd,lr,svc]:
            self.clf = OneVsRestClassifier(classifier)
            self.clf.fit(X_train,y_train)
            y_pred = self.clf.predict(X_test)
            self.print_score(y_pred,classifier)
    
    def classify(self,sentence):
        sentence = find_svo(sentence)
        sentence = ' '.join(sentence)
        print(sentence)
        x = [sentence]
        xt = self.tfidf.transform(x)
        prediction = self.clf.predict(xt)
        try:
            prediction_text = self.multilabel.inverse_transform(prediction)[0][0]
        except:
            prediction_text = 'ERROR ALERT!'
        return prediction_text



    def print_score(self,y_pred,clf):
        print("clf: ", clf.__class__.__name__)
        print('Jaccard Score: {}'.format(self.j_score(self.y_test,y_pred)))
        print('-------')
