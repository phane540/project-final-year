import io
from json import encoder
from flask import Flask,render_template,request,redirect,url_for,session,flash
import sqlite3
from email_validator import validate_email,EmailNotValidError



import csv
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import keras
import tensorflow as tf
import flask
from flask import Flask, render_template, request
from keras.models import load_model
import librosa
import pickle

import librosa
import librosa.display as lplt


# import matplotlib to be able to display graphs
import matplotlib.pyplot as plt

# transform .wav into .csv
import csv
import os
import numpy as np
import pandas as pd

# preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# model
import keras
import tensorflow as tf

#import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from joblib import load


from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import wikipedia
import matplotlib.pyplot as plt
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import base64
from matplotlib.pyplot import axes
import urllib.parse
import requests

scaler = load('scaler.joblib')
model = load('model.joblib')
encoder= load('encoder.joblib')



def check_username(user_name):
    con = sqlite3.connect('cse123.db')
    cur=con.cursor()
    cur.execute('select username from students where username=?',[user_name])
    nam=cur.fetchall()
    if len(nam)!=0:
        return True
    else:
        return False
def check_user(user_name,password):
    conn = sqlite3.connect('cse123.db')
    cur=conn.cursor()
    cur.execute("select username,enterpass  from students where username=? and enterpass=?",(user_name,password))
    data=cur.fetchall()
    
         
    if len(data)!=0:
        return True
    else:
        return False
def check_mail(mail):
    try:
        v=validate_email(mail)
        mail=v["email"]
        if 'gmail.com' in mail:
            return False
        elif 'acoe.edu.in' in mail:
            return False
        elif 'yahoo.com' in mail:
            return False
        return False
    except EmailNotValidError:
        return False


def check_mobile(mobile):
    if len(mobile)!=10:
        return True
    else:
        return False






    
app = Flask(__name__)
app.secret_key='hello'

@app.route('/')
def home():
    return render_template('nwp.html')
  
@app.route('/register',methods=["GET","POST"])
def register():
    if request.method=='POST':    
        user_name=request.form['n']
        pass_word=request.form['p']
        mail=request.form['gm']
        mobile=request.form['pn']
       
          
    
        conn = sqlite3.connect('cse123.db')
        conn.cursor()
        if check_username(user_name):
            return('username already exists , please try another username')
        elif check_mail(mail):
            return("incorrect email")
        elif check_mobile(mobile):
            return ('incorrect mobile number')
        
        
        conn.execute("INSERT INTO students(username, email, enterpass,mobile) values(?,?,?,?)",(user_name,mail,pass_word,mobile))
        conn.commit()
        conn.close()
        return render_template('nlog.html')
    
    return render_template('nreg.html')



@app.route('/predict',methods=['GET',"POST"])
def predict():
    global r
    r=None
    if request.method=='POST':   
        f = request.files['sound']
                # Load audio file
       
        # Retrieve user input data
        header_test = "filename length chroma_stft_mean chroma_stft_var rms_mean rms_var spectral_centroid_mean spectral_centroid_var spectral_bandwidth_mean \
                spectral_bandwidth_var rolloff_mean rolloff_var zero_crossing_rate_mean zero_crossing_rate_var harmony_mean harmony_var perceptr_mean perceptr_var tempo mfcc1_mean mfcc1_var mfcc2_mean \
                mfcc2_var mfcc3_mean mfcc3_var mfcc4_mean mfcc4_var".split()
                
        file = open('data_test.csv', 'w', newline = '')
        with file:
            writer = csv.writer(file)
            writer.writerow(header_test)
                
                
            #scaler = StandardScaler()
            
            #encoder = OneHotEncoder(categories='auto')
        
        sound_name = f
        y, sr = librosa.load(sound_name, mono = True, duration = 30)
        chroma_stft = librosa.feature.chroma_stft(y = y, sr = sr)
        rmse = librosa.feature.rms(y = y)
        spec_cent = librosa.feature.spectral_centroid(y = y, sr = sr)
        spec_bw = librosa.feature.spectral_bandwidth(y = y, sr = sr)
        rolloff = librosa.feature.spectral_rolloff(y = y, sr = sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        mfcc = librosa.feature.mfcc(y = y, sr = sr)
        to_append = f'{f.filename} {np.mean(chroma_stft)} {np.mean(rmse)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'

        for e in mfcc:
            to_append += f' {np.mean(e)}'

        file = open('data_test.csv', 'a', newline = '')

        with file:
            writer = csv.writer(file)
            writer.writerow(to_append.split())
                
        df_test = pd.read_csv('data_test.csv')
        
        
        
        print(df_test)
        #scaler.fit(df_test.iloc[:, 1:27])
        X_test = scaler.transform(np.array(df_test.iloc[:, 1:27]))

        print("X_test:", X_test)
        
        # Make prediction with the trained model
        prediction = model.predict(X_test)
        print(prediction)
        classes = np.argmax(prediction, axis = 1)
        print(classes)
        
        #encoder.fit(classes.reshape(-1,1))
        result = encoder.inverse_transform(classes.reshape(-1,))
        print(result)
        
    
        r=str(result[0])

    return render_template('predict.html',r=r)



@app.route('/results',methods=['POST','GET'])
def results():
    whale=r
    wikipedia.set_lang("en")

    # Get the page object for the Wikipedia article
    page = wikipedia.page(whale)

    # Get the introduction part of the article
    introduction = page.summary
        # Create a new Chrome browser window in headless mode
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome('C:/Users/phane/project final year/chromedriver_win32/chromedriver', options=options)

    # Navigate to the Wikipedia page for Humpback Whale

    driver.get(f"https://en.wikipedia.org/wiki/{whale}")

    # Get the page source and create a BeautifulSoup object
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all the headings on the page
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    # Initialize the page content variable as a list of sections
    sections = []

# Loop through each heading and its section text, and add it to the sections list
    for heading in headings:
        section_heading = heading.text.strip()
        
        section_heading=section_heading.replace("[edit]", "").replace("[0]","")
        section_text = ''

        # Find the section's text by looking at all the elements until the next heading
        next_node = heading.next_sibling
        while next_node and next_node.name not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            if next_node.name == 'p':
                section_text += '\n' + next_node.text.strip()
            next_node = next_node.next_sibling
        if section_text:
        
        # Add the section to the list
            sections.append({'heading': section_heading, 'text': section_text})
        # Close the browser window
    driver.quit()
    print(sections)

    
    return render_template('Output.html',introduction=introduction,sections=sections,whale=whale)






@app.route('/login', methods=["GET","POST"])
def login():
    
    if request.method=='POST':  
        user_name=request.form['n']
        password=request.form['p']
       
        if check_user(user_name,password):
            session['user']=user_name
            return redirect(url_for('user'))
        else:
            return ('username or password is incorrect')
    else:
        if 'user' in session:
            return redirect(url_for('user'))
       
    return render_template('nlog.html')

@app.route('/user',methods=['GET','POST'])
def user():
    if 'user' in session:
        user=session['user']
        print(user)
        return redirect(url_for('predict'))
    else:
        return redirect(url_for('login'))    
@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('user',None)
    return redirect(url_for("login"))
if __name__ == '__main__':
    app.run(debug=True)