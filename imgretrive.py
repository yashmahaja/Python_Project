import mysql.connector
from PIL import Image
from io import BytesIO 
import PIL.Image

db = mysql.connector.connect(user='root', password='13221@INDia',
                              host='localhost',
                              database='cpp')

cursor=db.cursor()
sql1='select image from images_demo where image_id=1'
db.commit()
cursor.execute(sql1)
data=cursor.fetchall()
file_like=BytesIO(data[0][0])
img=PIL.Image.open(file_like)
img.show()
db.close()