from logging import info
from flask import Flask, render_template,request,redirect,session,url_for
import MySQLdb 
from flask_mysqldb import MySQL
import random
import numpy as np
import pickle
import json
from flask import Flask, render_template, request
from flask_ngrok import run_with_ngrok
import nltk
from keras.models import load_model
from nltk.stem import WordNetLemmatizer

app=Flask(__name__)
app.secret_key="ebcqaeyzfqtgtai"

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="root"
app.config["MYSQL_DB"]="data"

db=MySQL(app)

@app.route('/',methods=['GET','POST'])

def index():
    if request.method == 'POST':
        if 'username' in request.form and 'password' in request.form:
            username=request.form['username']
            password=request.form['password']
            cursor=db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM info1 WHERE name_user=%s AND password_user=%s",(username,password))
            
        info=cursor.fetchone()
        if info is not None:
            if info['name_user'] == username and info['password_user'] == password:
                return redirect(url_for("myhome"))
        else:
             return render_template("index.html",message1="Password or username didn't match")
    return render_template("index.html")


@app.route('/signup.html',methods=['GET','POST'])

def register():
    if request.method == 'POST':

        if 'username' in request.form and 'password' in request.form and 'email' in request.form and 'phone' in request.form and 'password1' in request.form and 'address' in request.form:

            username=request.form['username']
            password1=request.form['password1']
            password=request.form['password']
            email=request.form['email']
            phone=request.form['phone']
            address=request.form['address']
            if password==password1:
                cursor=db.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("INSERT INTO data.info1(name_user,password_user,email_user,phone_user,address_user) VALUES(%s,%s,%s,%s,%s)",(username,password1,email,phone,address))
                db.connection.commit()
                return redirect(url_for("index"))
            else:
                return render_template("signup.html",message="Password didn't match")
        else:
            return "Enter all values"

    return render_template("signup.html")

#authentication

@app.route('/myprofile.html',methods=['GET','POST'])

def myprofile():
    if request.method == 'POST':
        return redirect(url_for("index"))

    return render_template("myprofile.html")


@app.route('/home.html',methods=['GET','POST'])

def myhome():
    if request.method == 'POST':
        if 'bname' in request.form and 'bemail' in request.form and 'brooms' in request.form and 'bdate' in request.form:
            bemail=request.form['bemail']
            brooms=request.form['brooms']
            bdate=request.form['bdate']
            cursor=db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("UPDATE data.info1 SET rooms_user=%s,date_user=%s WHERE email_user=%s",(brooms,bdate,bemail))
            db.connection.commit()
            return redirect(url_for("myreciept"))
    # get value of username & set value to username
    return render_template("home.html")

@app.route('/notification.html',methods=['GET','POST'])

def mynotification():
    return render_template("notification.html")


@app.route('/reciept.html',methods=['GET','POST'])
def myreciept():
    # get values from database & set values to card
    return render_template("reciept.html")


@app.route('/wishlist.html',methods=['GET','POST'])
def mywishlist():
    return render_template("wishlist.html")


@app.route('/bookingform',methods=['GET','POST'])

def mybooking():
    return render_template("reciept.html")

lemmatizer = WordNetLemmatizer()

model = load_model("chatbot_model.h5")
intents = json.loads(open("intents.json").read())
words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))

@app.route("/chatbot.html")
def home():
    return render_template("chatbot.html")


@app.route("/get", methods=["POST"])
def chatbot_response():
    msg = request.form["msg"]
    #checks is a user has given a name, in order to give a personalized feedback
    if msg.startswith('my name is'):
        name = msg[11:]
        ints = predict_class(msg, model)
        res1 = getResponse(ints, intents)
        res =res1.replace("{n}",name)
    elif msg.startswith('hi my name is'):
        name = msg[14:]
        ints = predict_class(msg, model)
        res1 = getResponse(ints, intents)
        res =res1.replace("{n}",name)
    #if no name is passed execute normally
    else:
        ints = predict_class(msg, model)
        res = getResponse(ints, intents)
    return res


# chat functionalities
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i["responses"])
            break
    return result



if __name__ == '__main__' :
    app.run(debug=True)


