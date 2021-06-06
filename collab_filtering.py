# %%
import pandas as pd
import numpy as np
import sqlite3
from scipy.sparse import csr_matrix
import sklearn
from sklearn.decomposition import TruncatedSVD

# %%
connR = sqlite3.connect('ratings (2).sqlite')
curR = connR.cursor()
curR.execute('SELECT user_id, book_id, rating FROM Ratings')
resultR = curR.fetchall()
columnR = ["user_id", "book_id", "rating"]
ratings = pd.DataFrame(resultR, columns=columnR)
ratings

# %%
connB = sqlite3.connect('bookdb.sqlite')
curB = connB.cursor()
curB.execute('SELECT book_id, Title FROM Book')
resultB = curB.fetchall()
columnB = ["book_id", "Title"]
books = pd.DataFrame(resultB, columns=columnB)
books

# %%
connU = sqlite3.connect('userdb.sqlite')
curU = connU.cursor()
curU.execute('SELECT user_id, Location, Age FROM User')
resultU = curU.fetchall()
columnU = ["user_id", "Location", "Age"]
users = pd.DataFrame(resultU, columns=columnU)
users

# %%
combine_book_rating = pd.merge(ratings, books, on='book_id')
combine_book_rating

# %%
combine_book_rating = combine_book_rating.dropna(axis=0, subset = ['Title'])

# %%
book_ratingCount = (combine_book_rating.groupby(by= ['Title'])['rating'].count().reset_index().rename(columns = {'rating': 'Total_Rating_Count'})[['Title', 'Total_Rating_Count']])
book_ratingCount

# %%
rating_with_total_rating = combine_book_rating.merge(book_ratingCount, left_on = 'Title', right_on = 'Title', how = 'left')
rating_with_total_rating

# %%
pd.set_option('display.float_format', lambda x: '%.3F' % x)
print(book_ratingCount['Total_Rating_Count'].describe())

# %%
print(book_ratingCount['Total_Rating_Count']. quantile(np.arange(.9, 1, .01))),

# %%
popularity_threshold = 50
rating_popular_book = rating_with_total_rating.query('Total_Rating_Count >- @popularity_threshold')
rating_popular_book

# %%
combined = rating_popular_book.merge(users, left_on = 'user_id', right_on = 'user_id', how = 'left')
us_canada_user_rating = combined[combined['Location'].str.contains("usa|canada")]
us_canada_user_rating = us_canada_user_rating.drop('Age', axis =1)
us_canada_user_rating

# %%
if not us_canada_user_rating[us_canada_user_rating.duplicated(['user_id', 'Title'])].empty:
    initial_rows = us_canada_user_rating.shape[0]
    
    print('Initial dataframeshape {0}'.format(us_canada_user_rating.shape))
    us_canada_user_rating = us_canada_user_rating.drop_duplicates(['user_id', 'Title'])
    current_rows = us_canada_user_rating.shape[0]
    print('New dataframe shape {0}'.format(us_canada_user_rating.shape))
    print('Removed {0} rows'.format(initial_rows - current_rows))

# %%
us_canada_user_rating_pivot = us_canada_user_rating.pivot(index = 'Title', columns = 'user_id', values = 'rating').fillna(0)
us_canada_user_rating_matrix = csr_matrix(us_canada_user_rating_pivot.values)

# %%
from sklearn.neighbors import NearestNeighbors

model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
model_knn.fit(us_canada_user_rating_matrix)

# %%
query_index = np.random.choice(us_canada_user_rating_pivot.shape[0])
distances, indices = model_knn.kneighbors(us_canada_user_rating_pivot.iloc[query_index, :].values.reshape(1,-1), n_neighbors = 10)
recom = []
for i in range(len(distances.flatten())):
    if i == 0:
        print('Recommendation for {0}:\n'.format(us_canada_user_rating_pivot.index[query_index]))
    else:
        #print('{0}: {1}, with distance of {2}'.format(i, us_canada_user_rating_pivot.index[indices.flatten()[i]], distances.flatten()[i]))
        recom.append(us_canada_user_rating_pivot.index[indices.flatten()[i]])
# %%


def recomendation():
    return recom