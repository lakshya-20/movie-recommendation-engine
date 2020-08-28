import pandas as pd
import numpy as np
print("Starting...")
movies_df=pd.read_csv('movies.csv')
movies_df.drop('title',1,inplace=True)
movies_df['genres']=movies_df.genres.str.split('|')
genres_df=movies_df.copy()
for index,row in movies_df.iterrows():
    for genre in row['genres']:
        genres_df.at[index,genre]=1
genres_df.drop('genres',1,inplace=True)
genres_df.fillna(0,inplace=True)
genres_df.to_csv('genres.csv',index=False)
genres_df=pd.read_csv('genres.csv')


userInput=[
    {'movieId':34,'rating':5.0},
    {'movieId':24,'rating':4.0},
    {'movieId':14,'rating':3.0},
    {'movieId':4,'rating':2.0},
    {'movieId':44,'rating':1.0}
]
userInput=pd.DataFrame(userInput)

userGenre=genres_df[genres_df['movieId'].isin(userInput['movieId'].tolist())]
userGenre.drop('movieId',1,inplace=True)
userGenre.reset_index(drop=True)
userProfile = userGenre.transpose().dot(userInput.rating.values)
genreTable=genres_df.copy()
genreTable.set_index('movieId',inplace=True)

recommend_df=((genreTable*userProfile).sum(axis=1))/(userProfile.sum())
recommend_df.sort_values(ascending=False,inplace=True)
print(recommend_df.head(5))
