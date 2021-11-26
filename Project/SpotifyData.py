import pandas as pd

# Using this kaggle dataset https://www.kaggle.com/lehaknarnauli/spotify-datasets that contains
# The data we need for our neural network such as popular artists, popular songs, length of songs, etc.

tracks_dataset = pd.read_csv('/Users/kennykim/Desktop/GitHub/Spotify Kaggle Data/tracks.csv')
artists_dataset = pd.read_csv('/Users/kennykim/Desktop/Github/Spotify Kaggle Data/artists.csv')