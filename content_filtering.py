# %%
import pandas as pd
import sqlite3
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

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
data = pd.merge(ratings, users, on = 'user_id', how = 'inner')
data

# %%
data = pd.merge(data, books, on = 'book_id', how = 'inner')
data

# %%
print('Number of books: ', data['book_id'].nunique())

# %%
print('Number of users: ', data['user_id'].nunique())

# %%
print('Missing data [%]')
round(data.isnull().sum() / len(data) * 100, 4)

# %%
sns.displot(data['Age'].dropna(), kde = False)

# %%
print('Number of outliers: ', sum(data['Age'] > 100))

# %%
data['rating'] = data['rating'].replace(0, None)

# %%
sns.countplot(x = 'rating', data = data)

# %%
print('Average book rating: ', round(data['rating'].mean(), 3))

# %%
country = data['Location'].apply(lambda row: str(row).split(',')[-1])
data.groupby(country)['rating'].count().sort_values(ascending = False).head(10)

# %%
data['Age'] = np.where(data['Age'] > 90, None, data['Age'])

# %%
median = data['Age'].median()
std = data['Age'].std()
is_null = data['Age'].isnull().sum()
rand_age = np.random.randint(median - std, median + std, size = is_null)
age_slice = data['Age'].copy()
age_slice[pd.isnull(age_slice)] = rand_age
data['Age'] = age_slice
data['Age'] = data['Age'].astype(int)
data

# %%
data['Country'] = data['Location'].apply(lambda row: str(row).split(',')[-1])

# %%
data = data.drop('Location', axis = 1)

# %%
data['Country']

# %%
df = data

# %%
df = df[df['rating'] >= 2]
df.shape

# %%
df.groupby('book_id')['user_id'].count().describe()

# %%
df = df.groupby('book_id').filter(lambda x: len(x) >= 5)
df.shape

# %%
df.groupby('user_id')['book_id'].count().describe()

# %%
df = df.groupby('user_id').filter(lambda x: len(x) >= 5)
df.shape

# %%
from tqdm import tqdm
from gensim.models import Word2Vec
import random

# %%
users = df['user_id'].unique().tolist()
len(users)

# %%
#shuffle user ids
random.shuffle(users)

# %%
users_train = [users[i] for i in range(round(0.9 * len(users)))]

# %%
#split data into train and validation set
train_df = df[df['user_id'].isin(users_train)]
validation_df = df[~df['user_id'].isin(users_train)]

# %%
#list to capture customer history
reads_train = []

#populate the list with the book ids
for i in tqdm(users_train):
    temp = train_df[train_df['user_id'] == i]['book_id'].tolist()
    reads_train.append(temp)

# %%
reads_val = []

for i in tqdm(validation_df['user_id'].unique()):
    temp = validation_df[validation_df['user_id'] == i]['book_id'].tolist()
    reads_val.append(temp)

# %%
#train word2vec model
model = Word2Vec(window = 10, sg = 1, hs = 0, negative = 10, alpha = 0.03, min_alpha = 0.0007, seed = 14)
model.build_vocab(reads_train, progress_per = 100)
model.train(reads_train, total_examples = model.corpus_count, epochs = 10, report_delay = 1)

# %%
model.init_sims(replace = True)
print(model)

# %%
#extract all vectors
X = model[model.wv.vocab]
X.shape

# %%
import umap.umap_ as umap

# %%
cluster_embedding = umap.UMAP(n_neighbors = 30, min_dist = 0.0, n_components = 2, random_state = 42).fit_transform(X)
plt.figure(figsize = (10, 9))
plt.scatter(cluster_embedding[:, 0], cluster_embedding[:, 1], s = 3, cmap = 'Spectral')

# %%
books = train_df[["book_id", "Title"]]

#remove duplicates
books.drop_duplicates(inplace = True, subset = 'book_id', keep = "last")

#create book-id and book-description on dictionary
books_dict = books.groupby('book_id')['Title'].apply(list).to_dict()

# %%
df[df['Title'].str.contains('Lord of the Rings')].sample()

# %%
books_dict['084238555X']

# %%
def similar_books(v, n =15):
    
    #extract most similar books for the input vector
    ms = model.similar_by_vector(v, topn = n+1)[1:]
    
    #extract name and similarity score of the similar products
    new_ms = []
    for j in ms:
        pair = books_dict[j[0]][0]
        new_ms.append(pair)
    
    return new_ms

# %%
print(model.wv.vocab.keys())


def crecom(bname):
    curB.execute('SELECT book_id FROM Book WHERE Title=?', (bname,))
    res = curB.fetchone()
    if res is None:
        x = random.choice(list(model.wv.vocab))
        r = str(x)
    else:
        r = str(res[0])
    return similar_books(model[r])

