import pandas as pd
import numpy as np
import pymongo
import itertools
from flask import Flask,request, url_for, redirect, render_template

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["flick"]

app=Flask(__name__)

@app.route('/initialize')
def initialize():
    mycol = mydb["genres_data"]
    mycol.drop()
    genres_df=pd.read_csv('genres.csv')
    genre_json=genres_df.to_json(orient='records')
    genre_json=eval(genre_json)
    genre_data=genre_json
    x = mycol.insert_many(genre_data)
    print("genres data synchronized")
    mycol = mydb["movies_data"]
    mycol.drop()
    movies_df=pd.read_csv('movies.csv')
    movies_json=movies_df.to_json(orient='records')
    movies_json=eval(movies_json)
    movies_data=movies_json
    movies_data[0]
    x = mycol.insert_many(movies_data)
    print("movies data synchronized")
    return "Initialized"

@app.route('/newReview')
def newReview():
    uid=1
    movieId=42
    rating=4
    mycol = mydb["reviews"]
    record={ "uid": uid, "movieId": movieId,"rating":rating }
    mycol.insert_one(record)
    #generating userInput table
    userInput=[]
    for x in mycol.find({"uid":uid},{ "_id": 0}):
      userInput.append(x)
    userInput=pd.DataFrame(userInput)
    userInput=userInput.drop(['uid'], axis = 1) 
    #fetching genres data from database
    mycol = mydb["genres_data"]
    data=[]
    for x in mycol.find({},{"_id":0}):
        data.append(x)
    genres_df=pd.DataFrame(data)
    #generating userProfile
    userGenre=genres_df[genres_df['movieId'].isin(userInput['movieId'].tolist())]
    userGenre.drop('movieId',1,inplace=True)
    userGenre.reset_index(drop=True)
    userProfile = userGenre.transpose().dot(userInput.rating.values)
    #getting new recommendations
    genreTable=genres_df.copy()
    genreTable.set_index('movieId',inplace=True)
    recommend_df=((genreTable*userProfile).sum(axis=1))/(userProfile.sum())
    recommend_df.sort_values(ascending=False,inplace=True)
    mycol = mydb["user_recommendation_data"]
    recommendation_json=eval(recommend_df.to_json())
    recommendation_data={"uid":1,"recommendation_data":recommendation_json}
    mycol.delete_one({"uid":uid})
    x = mycol.insert_one(recommendation_data)
    return "Review added"

@app.route('/recommendation')
def recommendation():
    mycol = mydb["user_recommendation_data"]
    x=mycol.find_one({"uid":1},{"_id":0})
    data=x['recommendation_data']
    # recommend_df=pd.Series(data)
    # recommend_df.head()
    data=dict(itertools.islice(data.items(),5))
    movies_id=list(data.keys())

    mycol=mydb['movies_data']

    movies_data=[]

    for i in mycol.find({},{"_id":0}):
        if(str(i["movieId"]) in movies_id):
            movies_data.append(i)
        #print(i["movieId"])
    movies_data=tuple(movies_data)
    re=(1,2,3)
    return "done"

if __name__=='__main__':
    app.run(debug=True)
