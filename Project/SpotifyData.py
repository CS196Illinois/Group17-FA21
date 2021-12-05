import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.indexes.base import Index
from sklearn.metrics.pairwise import cosine_similarity
import spotipy as spotify


from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA


# Using a kaggle dataset which categorizes the spotify data into data by year and data by genres as well

dataset = pd.read_csv('/Users/kennykim/Desktop/GitHub/Spotify Kaggle Data/data.csv')
dataset_year = pd.read_csv('/Users/kennykim/Desktop/Github/Spotify Kaggle Data/data_by_year.csv')
dataset_genres = pd.read_csv('/Users/kennykim/Desktop/GitHub/Spotify Kaggle Data/data_by_genres.csv')
#   provides the info of each datset : dataset.info(), dataset_year.info(), dataset_genres.info()

x = dataset.select_dtypes(include='number')

# This graph below uses the elbow method to determine the optimal number of clusters to use in the kmeans function
# Plotting it with the spotify dataset filtered to only hold scalar values, we can determine the "elbow" of the graph to be 7
# sum_of_dist = []
# k_range = range(1,20)
# for i in k_range:
#     kmeans = KMeans(i)
#     kmeans.fit(x)
#     sum_of_dist.append(kmeans.inertia_)
    
# plt.plot(k_range, sum_of_dist, 'bx-')
# plt.xlabel('K Values')
# plt.ylabel('Inertia')
# plt.title('Elbow Test')
# plt.show()

pca = PCA(2)
df = pca.fit_transform(x)
kmeans = KMeans(7)
labels = kmeans.fit_predict(df)

# KMeans Clustering Visual using n_clusters = 7

# u_labels = np.unique(label)

# for i in u_labels:
#     plt.scatter(df[label == i , 0] , df[label == i , 1] , label = i)
# plt.legend()
# plt.show()
def cluster_indices(cluster_number, labels):
    return np.where(labels == cluster_number)[0]

def song_data(song, dataset):
    try:
        data = dataset[(dataset['name'] == song['name']) & dataset['id'] == song['id']]
        return data.select_dtypes(include='number')
    except IndexError:
        data = spotify.find_song(song['name'], song['id'])
        return data.select_dtypes(include='number')
    







