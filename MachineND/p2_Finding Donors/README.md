# finding_donors

Original title: Machine learning ND 1, supervised learning.md

Original published date: 2016-12-25 at blogspot

Original dataset at [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Census+Income).

- 45 k instances
- 14 attributes (including one binary lable feature:income class)

Machine learning books: https://www.analyticsvidhya.com/blog/2015/10/read-books-for-beginners-machine-learning-artificial-intelligence/



**Features**

- `age`: Age
- `workclass`: Working Class (Private, Self-emp-not-inc, Self-emp-inc, Federal-gov, Local-gov, State-gov, Without-pay, Never-worked)
- `education_level`: Level of Education (Bachelors, Some-college, 11th, HS-grad, Prof-school, Assoc-acdm, Assoc-voc, 9th, 7th-8th, 12th, Masters, 1st-4th, 10th, Doctorate, 5th-6th, Preschool)
- `education-num`: Number of educational years completed
- `marital-status`: Marital status (Married-civ-spouse, Divorced, Never-married, Separated, Widowed, Married-spouse-absent, Married-AF-spouse)
- `occupation`: Work Occupation (Tech-support, Craft-repair, Other-service, Sales, Exec-managerial, Prof-specialty, Handlers-cleaners, Machine-op-inspct, Adm-clerical, Farming-fishing, Transport-moving, Priv-house-serv, Protective-serv, Armed-Forces)
- `relationship`: Relationship Status (Wife, Own-child, Husband, Not-in-family, Other-relative, Unmarried)
- `race`: Race (White, Asian-Pac-Islander, Amer-Indian-Eskimo, Other, Black)
- `sex`: Sex (Female, Male)
- `capital-gain`: Monetary Capital Gains
- `capital-loss`: Monetary Capital Losses
- `hours-per-week`: Average Hours Per Week Worked
- `native-country`: Native Country (United-States, Cambodia, England, Puerto-Rico, Canada, Germany, Outlying-US(Guam-USVI-etc), India, Japan, Greece, South, China, Cuba, Iran, Honduras, Philippines, Italy, Poland, Jamaica, Vietnam, Mexico, Portugal, Ireland, France, Dominican-Republic, Laos, Ecuador, Taiwan, Haiti, Columbia, Hungary, Guatemala, Nicaragua, Scotland, Thailand, Yugoslavia, El-Salvador, Trinadad&Tobago, Peru, Hong, Holand-Netherlands)

**Target Variable**

- `income`: Income Class (<=50K, >50K)



## workflow

1. feature scaling for [‘capital-gain’, ‘capital-loss’].`df.apply(lambda x: np.log(x + 1))`
2. feature scaling for [‘age’, ‘education-num’, ‘capital-gain’, ‘capital-loss’, ‘hours-per-week’] `sklearn.preprocessing.MinMaxScaler.fit_transform(df)`
3. one hot encode: `pd.get_dummies (df)`
4. `sklearn.model_selection.train_test_split()`
5. fit, predict, `sklearn.metrics.accuracy_score(y_test,y_predict)`
6. `sklearn.grid_search.GridSearchCV`
7. feature importance. It’s interesting that different models have different preferences.



```python
import numpy as np
import pandas as pd
# Split the data into features and target label
income_raw = data['income']
features_raw = data.drop('income', axis = 1)
# Log-transform the skewed features
skewed = ['capital-gain', 'capital-loss']
features_raw[skewed] = data[skewed].apply(lambda x: np.log(x + 1))
# Import sklearn.preprocessing.StandardScaler
from sklearn.preprocessing import MinMaxScaler

# Initialize a scaler, then apply it to the features
scaler = MinMaxScaler()
numerical = ['age', 'education-num', 'capital-gain', 'capital-loss', 'hours-per-week']
features_raw[numerical] = scaler.fit_transform(data[numerical])

# One-hot encode 
features = pd.get_dummies(features_raw)
income = pd.get_dummies(income_raw)['>50K']
# count 
# look at first few non-numeric columns
for col in data.columns[:5]:
    if data[col].dtype == 'O':
        display(data[col].value_counts())
```

### grid search

```python
from sklearn.grid_search import GridSearchCV 
from sklearn.metrics import make_scorer
clf = SVC()
param_grid = {'kernel':('linear', 'rbf'), 'C':[1, 10,100]}
scorer = make_scorer(fbeta_score, beta=0.5)
grid_obj = GridSearchCV(clf, param_grid,scoring = scorer)
grid_fit = grid_obj.fit(X_train,y_train)
best_clf = grid_fit.best_estimator_
predictions = (clf.fit(X_train, y_train)).predict(X_test)
best_predictions = best_clf.predict(X_test)
```

### feature importance

```python
# only certian supervised learning model has the attribute 'feature_importances_'
from sklearn.tree import DecisionTreeClassifier 
model = DecisionTreeClassifier()
model.fit(X_train, y_train)
importances = model.feature_importances_
vs.feature_plot(importances, X_train, y_train)

# look at top "n" feature importances
n = 10
fi = model.feature_importances_
pd.Series(fi, index=X_train.columns).sort_values(ascending=False)[:n].plot(kind='bar');
```

# [sebastian raschka](https://sebastianraschka.com/)

https://sebastianraschka.com/faq/index.html

## software engineering vs machine learning

**traditional programming:**

- set of rules + data -> computer -> results

**machine learning:**

- results + data -> machine learning algorithm + computer -> set of rules

**Or in other words, machine learning is about finding the optimal instructions to automate a task. Machine learning algorithms are instructions for computers to learn other instructions automatically from data or experience. Therefore, machine learning is the automation of automation.**

## recommended curriculum

- Andrew Ng’s [Machine Learning course on Coursera](https://class.coursera.org/ml-005/lecture)
- P.-N. Tan, M. Steinbach, and V. Kumar. [Introduction to Data Mining](http://www-users.cs.umn.edu/~kumar/dmbook/index.php), (First Edition). Addison-Wesley Longman Publishing Co., Inc., Boston, MA, USA, 2005.
- his book: python machine learning

While you work on your individual projects, I would maybe deepen your (statistical learning) knowledge via one of the three below:

- T. Hastie, R. Tibshirani, J. Friedman, T. Hastie, J. Friedman, and R. Tibshirani. [The Elements of Statistical Learning](http://statweb.stanford.edu/~tibs/ElemStatLearn/), volume 2. Springer, 2009.
- C. M. Bishop et al. [Pattern recognition and machine learning](http://www.springer.com/us/book/9780387310732), volume 1. springer New York, 2006.
- Duda, Richard O., Peter E. Hart, and David G. Stork. [Pattern classification](http://www.wiley.com/WileyCDA/WileyTitle/productCd-0471056693.html). John Wiley & Sons, 2012.

## "real-world" application vs Kaggle

In practice, it often boils down to finding the sweet spot between meeting the project deadline high predictive performance high computational efficiency good interpretability These aspects differ from project to project, and **it is really important to be clear about what you are trying to achieve beforehand**.

[example ML notebook](http://nbviewer.jupyter.org/github/rhiever/Data-Analysis-and-Machine-Learning-Projects/blob/master/example-data-science-notebook/Example%20Machine%20Learning%20Notebook.ipynb). Use seaborn analyze iris.



