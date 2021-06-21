from logging import info
from flask import Flask, render_template,request,redirect,session,url_for
import MySQLdb 
from flask_mysqldb import MySQL


islogin=False


app=Flask(__name__)
app.secret_key="ebcqaeyzfqtgtai"

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="13221@INDia"
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
        else:
            return "Enter all values"
            
        info=cursor.fetchone()
        if info is not None:
            if info['name_user'] == username and info['password_user'] == password:
                return render_template("home.html")
        else:
            return "unsuccsesful"
    return render_template("index.html")


# islogin=index()

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
                cursor.execute("INSERT INTO data.info1 VALUES(%s,%s,%s,%s,%s)",(username,password1,email,phone,address))
                db.connection.commit()
                return "signup succesful"
            else:
                return "password not match"
        else:
            return "Enter all values"


    return render_template("signup.html")


#authontication


@app.route('/myprofile.html',methods=['GET','POST'])

def myprofile():
    return render_template("myprofile.html")


@app.route('/home.html',methods=['GET','POST'])

def myhome():
    return render_template("home.html")



if __name__ == '__main__' :
    app.run(debug=True)


