import pandas as pd
import numpy as np
import pymongo
import itertools
import csv
import json
from bson import json_util
from flask import Flask,request, url_for, redirect, render_template,jsonify,Response
from flask_cors import CORS, cross_origin

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#update mongodbURL for production
mydb = myclient["flick"]

app=Flask(__name__)
cors = CORS(app)


@app.route('/')
@cross_origin()
def hello_world():
    return 'Hello World!'

@app.route('/initialize')
@cross_origin()
def initialize():
    mycol = mydb["genres_datas"]
    mycol.drop()
    genres_df=pd.read_csv('genres.csv')
    genre_json=genres_df.to_json(orient='records')
    genre_json=eval(genre_json)
    genre_data=genre_json
    x = mycol.insert_many(genre_data)
    print("Genres data synchronized "+str(mydb.genres_datas.count_documents({})))

    mycol=mydb["movies_datas"]
    mycol.drop()
    csvfile = open('movies.csv', 'r',encoding='utf-8')
    reader = csv.DictReader( csvfile )
    header=["movieId","imdb_link","poster","title","imdb_score","genres"]
    for each in reader:
        row={}
        for field in header:
            row[field]=each[field]
        #print("Inserting a movie"+str(mycol.find().count()))    
        mycol.insert_one(row)
    print("movies data synchronized "+str(mydb.movies_datas.count_documents({})))
    return "Initialized"

@app.route('/newReview/<uid>')
@cross_origin()
def newReview(uid):
    mycol = mydb["reviews"]
    print(uid)
    #record={ "uid": uid, "movieId": movieId,"rating":rating }
    #mycol.insert_one(record)
    #generating userInput table
    userInput=[]
    for x in mycol.find({"userId":uid},{ "_id": 0}):
      userInput.append(x)
    userInput=pd.DataFrame(userInput)
    userInput=userInput.drop(['userId','comment'], axis = 1) 
    #fetching genres data from database
    mycol = mydb["genres_datas"]
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
    mycol = mydb["user_recommendation_datas"]
    recommendation_json=eval(recommend_df.to_json())
    recommendation_data={"uid":uid,"recommendation_data":recommendation_json}
    mycol.delete_one({"uid":uid})
    x = mycol.insert_one(recommendation_data)
    print("Review added")
    return jsonify("Review added")

@app.route('/recommendation/<uid>')
@cross_origin()
def recommendation(uid):
    #uid=int(uid)
    print(uid)
    mycol = mydb["user_recommendation_datas"]
    x=mycol.find_one({"uid":uid},{"_id":0})
    data=x['recommendation_data']
    # recommend_df=pd.Series(data)
    # recommend_df.head()
    data=dict(itertools.islice(data.items(),10))
    movies_id=list(data.keys())

    mycol=mydb['movies_datas']
    movies_data=[]
    for i in mycol.find({}):
        if(str(i["movieId"]) in movies_id):
            movies_data.append(i)
    print("Returened data")
    #return json_response(movies_data)
    
    return Response(
        json_util.dumps(movies_data),
        mimetype='application/json'
    )
    


def json_response(payload, status=200):
    return (json.dumps(payload), status, {'content-type': 'application/json'})
if __name__=='__main__':
    app.run()
