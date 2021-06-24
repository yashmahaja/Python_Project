from logging import info
from flask import Flask, render_template,request,redirect,session,url_for
import MySQLdb 
from flask_mysqldb import MySQL

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

if __name__ == '__main__' :
    app.run(debug=True)


