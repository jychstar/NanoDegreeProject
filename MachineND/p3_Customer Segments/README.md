# Customer segments

original title: Machine Learning ND 2, unsupervised learning

original post date: 2017-2-10

Original dataset is hosted at [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Wholesale+customers).

- 440 instances
- 8 attributes

**Attribute Information:**

1)	FRESH: annual spending (m.u.) on fresh products (Continuous); 
2)	MILK: annual spending (m.u.) on milk products (Continuous); 
3)	GROCERY: annual spending (m.u.)on grocery products (Continuous); 
4)	FROZEN: annual spending (m.u.)on frozen products (Continuous) 
5)	DETERGENTS_PAPER: annual spending (m.u.) on detergents and paper products (Continuous) 
6)	DELICATESSEN: annual spending (m.u.)on and delicatessen products (Continuous); 
7)	CHANNEL: customersâ€™ Channel - Horeca (Hotel/Restaurant/CafÃ©) or Retail channel (Nominal) 
8)	REGION: customersâ€™ Region â€“ Lisnon, Oporto or Other (Nominal) 

**Descriptive Statistics:** 
(Minimum, Maximum, Mean, Std. Deviation) 
FRESH (	3, 112151, 12000.30, 12647.329) 
MILK	(55, 73498, 5796.27, 7380.377) 
GROCERY	(3, 92780, 7951.28, 9503.163) 
FROZEN	(25, 60869, 3071.93, 4854.673) 
DETERGENTS_PAPER (3, 40827, 2881.49, 4767.854) 
DELICATESSEN (3, 47943, 1524.87, 2820.106) 
**REGION	Frequency** 
Lisbon	77 
Oporto	47 
Other Region	316 
Total	440 
**CHANNEL	Frequency** 
Horeca	298 
Retail	142 
Total	440 



**Horeca** (also **HoReCa**, **HORECA**) is an abbreviation used in Europe for the food service industry. The term is a syllabic abbreviation of the words Hotel/Restaurant/Café

Udacity intentionally removed "channel" and Region" features to make it an unsupervised learning task. All these 6 attributes are numerical data.

## Data preprocessing

useful codes:

```python
data = pd.read_csv("customers.csv")
data.drop(['Region', 'Channel'], axis = 1, inplace = True)

data.info()
data.median()
data.describe()
data.plot.box(vert=False)
sns.boxplot(data)

from sklearn import preprocessing
samples_standard = preprocessing.StandardScaler().fit(data).transform(samples)
pd.DataFrame(samples_standard).plot.bar(figsize=(10,4), title='Samples compared to Standard distribution', grid=True)
```

Decision tree regressor, a way to find the relationship between variables.

```python
target = 'Grocery'
new_input = data.drop([target],axis=1)
new_output = data[target]

from sklearn.model_selection import train_test_split 
X_train, X_test, y_train, y_test = train_test_split(new_input, new_output, test_size=0.25, random_state=0)

from sklearn.tree import DecisionTreeRegressor
regressor = DecisionTreeRegressor(random_state=0)
regressor.fit(X_train,y_train)

regressor.score(X_test,y_test)
```



draw correlation map

```python
corr = data.corr()
# remove first row and last column for a cleaner look
first_row, last_col = corr.columns[[0,-1]]
corr.drop(first_row, axis=0, inplace=True)
corr.drop( last_col, axis=1, inplace=True)
mask = np.zeros_like(corr)  # use a mask to hide the redundance value
mask[np.triu_indices_from(mask, k=1)] = True # use indices for the upper-triangle of array, k is offset
# plot the heatmap
with sns.axes_style("white"):
    sns.heatmap(corr, mask=mask, annot=True, cmap='RdBu', fmt='+.2f', cbar=False)
```

feature scaling

```python
log_data = np.log(data)
```

outlier detection and remove

```python
from collections import Counter
c= Counter()
for feature in log_data.keys():
    Q1 = np.percentile(log_data[feature],25)
    Q3 = np.percentile(log_data[feature],75)
    step = 1.5*(Q3-Q1)
    d = dict((log_data[feature] < Q1 - step) | (log_data[feature] > Q3 + step)) # convert to dictionary (index: bool)
    c.subtract(Counter(d))
print "data points that are considered outliers for more than one feature:"
outliers=[]
for key in c:
    if c[key] <= -2:
        outliers.append(key)
print outliers
good_data = log_data.drop(log_data.index[outliers]).reset_index(drop = True)
```

Data is ready for PCA:

- discover which dimensions about the data best maximize the variance of features involved. 
- PCA will also report the *explained variance ratio* of each dimension — how much variance within the data is explained by that dimension alone.

```python
from sklearn.decomposition import PCA
pca = PCA(n_components=6) # how many components will be shown regardless the actual components
pca.fit(data)  # input features
print np.cumsum(pca.explained_variance_ratio_) # feature variance
print pca.components_.shape # new features as a linear combination of old features

```
only use 2 components for easy visualization and clustering:

```python
reduced_data= PCA(n_componets=2).fit(data).transform(data)
```

biplot

```python
def biplot(columns, reduced_data, pca):
    fig, ax = plt.subplots(figsize = (14,8))
    # scatterplot of the reduced data
    ax.scatter(x=reduced_data.loc[:, 'Dimension 1'], y=reduced_data.loc[:, 'Dimension 2'],
        facecolors='b', edgecolors='b', s=70, alpha=0.5)
    feature_vectors = pca.components_.T
    # we use scaling factors to make the arrows easier to see
    arrow_size, text_pos = 7.0, 8.0
    # projections of the original features
    for i, v in enumerate(feature_vectors):
        ax.arrow(0, 0, arrow_size*v[0], arrow_size*v[1],
                  head_width=0.2, head_length=0.2, linewidth=2, color='red')
        ax.text(v[0]*text_pos, v[1]*text_pos, columns[i], color='black',
                 ha='center', va='center', fontsize=18)

    ax.set_xlabel("Dimension 1", fontsize=14)
    ax.set_ylabel("Dimension 2", fontsize=14)
    ax.set_title("PC plane with original feature projections.", fontsize=16);
    plt.show()
biplot(good_data.columns, reduced_data, pca)
```

## k-means clustering and silhouette score

The [silhouette coefficient](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html) for a data point measures how similar it is to its assigned cluster from -1 (dissimilar) to 1 (similar). Calculating the *mean* silhouette coefficient provides for a simple scoring method of a given clustering.

```python
from sklearn.cluster import KMeans
clusterer = KMeans(n_clusters=2, random_state=0).fit(reduced_data)
preds = clusterer.predict(reduced_data)
centers = clusterer.cluster_centers_
print 'centers:', centers
from sklearn.metrics import silhouette_score
print "silhouette_score: ", silhouette_score(reduced_data,preds)
```

try different number of clustering using 2 PCs

```python
clusters = range(2, 7)
scores = []
for k in clusters:
    clusterer = KMeans(n_clusters=k, random_state=0).fit(reduced_data)
    preds = clusterer.predict(reduced_data)
    scores.append(silhouette_score(reduced_data,preds))    
plt.plot(clusters,scores,'--ob')
plt.xlabel('number of clusters')
plt.ylabel('silhouette score')
```

data recovery:

```python
log_centers = pca.inverse_transform(centers)  # (2,2) -> (2,6)
true_centers = np.exp(log_centers)/data.median().values
true_centers = pd.DataFrame(np.round(true_centers,2), columns = data.keys(), 
             index= ['Segment {}'.format(i) for i in range(0,len(centers))])
true_centers = true_centers.append(data.describe().ix['50%']/data.median().values)
true_centers.plot(kind = 'bar', figsize = (16, 4))
display(true_centers)
```



add original channel and verify unsupervised learning results

```python
def channel_results(reduced_data, outliers, pca_samples):
	try:
	    full_data = pd.read_csv("customers.csv")
	except:
	    print "Dataset could not be loaded. Is the file missing?"
	    return False
	channel = pd.DataFrame(full_data['Channel'], columns = ['Channel'])
	channel = channel.drop(channel.index[outliers]).reset_index(drop = True)
	labeled = pd.concat([reduced_data, channel], axis = 1)
	fig, ax = plt.subplots(figsize = (14,8))
	cmap = cm.get_cmap('gist_rainbow')

	# Color the points based on assigned Channel
	labels = ['Hotel/Restaurant/Cafe', 'Retailer']
	grouped = labeled.groupby('Channel')
	for i, channel in grouped:
	    channel.plot(ax = ax, kind = 'scatter', x = 'Dimension 1', y = 'Dimension 2', \
	                 color = cmap((i-1)*1.0/2), label = labels[i-1], s=30);

	# Plot transformed sample points
	for i, sample in enumerate(pca_samples):
		ax.scatter(x = sample[0], y = sample[1], \
	           s = 200, linewidth = 3, color = 'black', marker = 'o', facecolors = 'none');
		ax.scatter(x = sample[0]+0.25, y = sample[1]+0.3, marker='$%d$'%(i), alpha = 1, s=125);

	# Set plot title
	ax.set_title("PCA-Reduced Data Labeled by 'Channel'\nTransformed Sample Data Circled");
channel_results(reduced_data, outliers, pca_samples)    
```

