import numpy as np
import pandas as pd
import sys
import time
from collections import Counter
import time
import pickle
from flask import Flask,request, url_for, redirect, render_template

app=Flask(__name__)



global vocab_size
vocab_size=0

def get_target(label):
    if(label=="POSITIVE"):
        return 1
    elif(label=="NEGATIVE"):
        return 0
    
def sigmoid(x):
    return (1/(1+np.exp(-x)))

def map_input(review,word2index,vocab_size=vocab_size):
    layer=np.zeros((1,vocab_size))
    for word in review.split(' '):
        if word in word2index.keys():
            layer[0][word2index[word]]=1
    return layer



w01=pickle.load(open('w01.txt','rb'))
w12=pickle.load(open('w12.txt','rb'))
w2i=pickle.load(open('w2i.txt','rb'))
global_accuracy=pickle.load(open('global_accuracy.txt','rb'))
vocab_size=pickle.load(open('vocab_size.txt','rb'))

@app.route('/train') 
def train(learning_rate=0.001,hidden_nodes=10,global_accuracy=global_accuracy):
    start_time=time.time()
    df=pd.read_csv('data.csv')
    reviews=df['Reviews'].tolist()
    labels=df['Labels'].tolist()

    print("Data Loaded")
    words=Counter()
    for i in range(len(reviews)):
        for word in reviews[i].split(' '):
            words[word]+=1
    vocab=set(words.keys())
    vocab_size=len(vocab)
    pickle.dump(vocab_size,open('vocab_size.txt','wb'))
    word2index={}
    for i,word in enumerate(vocab):
        word2index[word]=i
    
    
    print("Word to Index Updated")
    correct=0
    accuracy=0
    start_time=time.time()
    weights_0_1=np.zeros((vocab_size,hidden_nodes))
    weights_1_2=np.random.normal(0.0,1,(hidden_nodes,1))
    del_0_1=np.zeros(weights_0_1.shape)
    del_1_2=np.zeros(weights_1_2.shape)
    for i in range(len(reviews)):
        review=reviews[i]
        label=labels[i]
        target=get_target(label)
        
        x=map_input(review,word2index,vocab_size)
        indices=set()
        for word in review.split(' '):
            indices.add(word2index[word])

        one_input=np.zeros((1,10))
        for index in indices:
            one_input += weights_0_1[index]
        one_output=one_input
        
        two_input=np.dot(one_output,weights_1_2)
        two_output=sigmoid(two_input)
        
        error=two_output-target
        two_error_term=error*two_output*(1-two_output)
        one_error_term=np.dot(two_error_term,weights_1_2.T)
        
        delta_1_2=two_error_term*one_output.T
        delta_0_1=one_error_term*x.T
        
        weights_1_2 -=learning_rate*delta_1_2
        weights_0_1 -=learning_rate*delta_0_1
        
        if(two_output >= 0.5 and label == 'POSITIVE'):
            correct += 1
        elif(two_output < 0.5 and label == 'NEGATIVE'):
            correct += 1
        
        elapsed_time = float(time.time() - start_time)
        if(i%1000==0):
            progress=(100 * i/(len(reviews)))
            accuracy=(correct * 100 / float(i+1))
            speed= i / elapsed_time if elapsed_time > 0 else 0
            print("Progess:{}  Correct:{} Accuracy:{} Speed:{}".format(progress,correct,accuracy,speed))
    if(global_accuracy<accuracy):
        pickle.dump(weights_0_1,open('w01.txt','wb'))
        pickle.dump(weights_1_2,open('w12.txt','wb'))
        pickle.dump(word2index,open('w2i.txt','wb'))
        w01=weights_0_1
        w10=weights_1_2
        w2i=word2index
        global_accuracy=accuracy
        print("Updated weights")
    else:
        print("Discarded")
        
    return "Trained Model and your modal took "+ str(time.time()-start_time)+" seconds to get trained."

@app.route('/predict/<review>')    
def prediction(review):
    weights_0_1=pickle.load(open('w01.txt','rb'))
    weights_1_2=pickle.load(open('w12.txt','rb'))
    w2i=pickle.load(open('w2i.txt','rb'))
    vocab_size=pickle.load(open('vocab_size.txt','rb'))
    x=map_input(review,w2i,vocab_size)
    print(x.shape)
    print(weights_0_1)
    one_input=np.dot(x,weights_0_1)
    one_output=one_input
    two_input=np.dot(one_output,weights_1_2)
    two_output=sigmoid(two_input)
    if(two_output>=0.5):
        output="POSITIVE"
    elif(two_output<0.5):
        output="NEGATIVE"
    return(output)

@app.route('/initialize')
def initialize():
    global_accuracy=0
    vocab_size=0
    weights_0_1=np.zeros((vocab_size,10))
    weights_1_2=np.random.normal(0.0,1,(10,1))
    word2index={}
    pickle.dump(global_accuracy,open('global_accuracy.txt','wb'))
    pickle.dump(vocab_size,open('vocab_size.txt','wb'))
    pickle.dump(weights_0_1,open('w01.txt','wb'))
    pickle.dump(weights_1_2,open('w12.txt','wb'))
    pickle.dump(word2index,open('w2i.txt','wb'))
    return "Done"

if __name__=='__main__':
    app.run(debug=True)
