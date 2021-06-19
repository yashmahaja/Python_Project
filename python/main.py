import mysql.connector
db= mysql.connector.connect(host='localhost',database='test',user='root',password='13221@INDia')
cursor=db.cursor()
sql= "SELECT * FROM table1"
cursor.execute(sql)
record = cursor.fetchone()
print(record)