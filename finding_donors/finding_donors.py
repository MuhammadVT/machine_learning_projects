# Explore the Data

# Import libraries necessary for this project
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from time import time
#from IPython.display import display # Allows the use of display() for DataFrames

# Import supplementary visualization code visuals.py
#import visuals as vs

# Pretty display for notebooks
#%matplotlib inline

# Load the Census dataset
data = pd.read_csv("census.csv")

# Success - Display the first record
#display(data.head(n=1))

# TODO: Total number of records
n_records = data.shape[0]

# TODO: Number of records where individual's income is more than $50,000
n_greater_50k = np.sum(data.income.apply(lambda x: x=='>50K'))

# TODO: Number of records where individual's income is at most $50,000
n_at_most_50k = np.sum(data.income.apply(lambda x: x=='<=50K'))

# TODO: Percentage of individuals whose income is more than $50,000
greater_percent = (1.0 * n_greater_50k) / n_records * 100.  

# Preparing the Data

# Transforming Skewed Continuous Features

# Split the data into features and target label
income_raw = data['income']
features_raw = data.drop('income', axis = 1)

# Log-transform the skewed features
skewed = ['capital-gain', 'capital-loss']
features_raw[skewed] = data[skewed].apply(lambda x: np.log(x + 1))


# Normalizing Numerical Features

# Import sklearn.preprocessing.StandardScaler
from sklearn.preprocessing import MinMaxScaler

# Initialize a scaler, then apply it to the features
scaler = MinMaxScaler()
numerical = ['age', 'education-num', 'capital-gain', 'capital-loss', 'hours-per-week']
features_raw[numerical] = scaler.fit_transform(data[numerical])

# TODO: One-hot encode the 'features_raw' data using pandas.get_dummies()
features = pd.get_dummies(features_raw)

# TODO: Encode the 'income_raw' data to numerical values
income = income_raw.apply(lambda x: 0 if x == '<=50K' else 1)

# Print the number of features after one-hot encoding
encoded = list(features.columns)

# Import train_test_split
from sklearn.cross_validation import train_test_split

# Split the 'features' and 'income' data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, income, test_size = 0.2, random_state = 0)



# Question 1 - Naive Predictor Performace
# TODO: Calculate accuracy
accuracy = greater_percent

# TODO: Calculate F-score using the formula above for beta = 0.5
precision = greater_percent / 100.
recall = 1.0
beta = 0.5
fscore = (1 + beta**2) * (precision * recall) / (beta**2 * precision + recall)

# Model Application
# Decision tree:
# 1. real-world application :  Decisoin tree has been used to classify three dimensional objects
#http://www.sciencedirect.com/science/article/pii/003132039390125G

# 2.  The strenghs of decision trees are:
# Simple to understand and to interpret, can be visualised.
# Requires little data preparation. No need to do feature normalisation, creating dummy variables, etc. 
# The cost of using the tree (i.e., predicting data) is logarithmic in the number of data points used to train the tree.
# Able to handle both numerical and categorical data. Also able to handle multi-output problems.
# Possible to validate a model using statistical tests.
# Performs well even if its assumptions are somewhat violated by the true model from which the data were generated.

#The disadvantages of decision trees include:

# Decision-tree learners can create over-complex trees that do not generalise the data well, thus cause overfitting. 
# Decision trees can be unstable because small variations in the data might result in a completely different tree being generated.
# The problem of learning an optimal decision tree is known to be NP-complete under several aspects of optimality and even for simple concepts. 
# There are concepts that are hard to learn because decision trees do not express them easily, such as XOR, parity or multiplexer problems.
# Decision tree learners create biased trees if some classes dominate.

# Decision tree is a good candidate for this problem because 

# 2. 
def train_predict(learner, sample_size, X_train, y_train, X_test, y_test): 
    '''
    inputs:
       - learner: the learning algorithm to be trained and predicted on
       - sample_size: the size of samples (number) to be drawn from training set
       - X_train: features training set
       - y_train: income training set
       - X_test: features testing set
       - y_test: income testing set
    '''
    
    results = {}
    
    # TODO: Fit the learner to the training data using slicing with 'sample_size'
    start = time() # Get start time
    learner = learner.fit(X_train[:sample_size], y_train[:sample_size])
    end = time() # Get end time
    
    # TODO: Calculate the training time
    results['train_time'] = end - start
        
    # TODO: Get the predictions on the test set,
    #       then get predictions on the first 300 training samples
    start = time() # Get start time
    predictions_test = learner.predict(X_test, y_test)
    predictions_train = learner.predict(X_train[:300], y_train[:300])
    end = time() # Get end time
    
    # TODO: Calculate the total prediction time
    results['pred_time'] = end-start
            
    # TODO: Compute accuracy on the first 300 training samples
    results['acc_train'] = accuracy_score(predictions_train, y_train[:300])
        
    # TODO: Compute accuracy on test set
    results['acc_test'] = accuracy_score(predictions_test, y_test)
    
    # TODO: Compute F-score on the the first 300 training samples
    results['f_train'] = fbeta_score(prediction_train, y_train[:300]) 
        
    # TODO: Compute F-score on the test set
    results['f_test'] = fbeta_score(prediction_test, y_test])
       
    # Success
    print "{} trained on {} samples.".format(learner.__class__.__name__, sample_size)
        
    # Return the results
    return results

