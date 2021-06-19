# import mysql.connector
# db= mysql.connector.connect(host='localhost',database='test',user='root',password='13221@INDia')
# cursor=db.cursor()
# sql= "SELECT * FROM table1"
# cursor.execute(sql)
# record = cursor.fetchone()
# print(record)

from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')

def index():
    return render_template("index.html")

@app.route('/signup.html')

def register():
    return render_template("signup.html")


if __name__ == '__main__' :
    app.run(debug=True)