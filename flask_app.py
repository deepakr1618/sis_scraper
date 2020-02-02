from manager.createChart import lightTheme , darkTheme
from manager.scraper import Parser , Scraper
from manager.firestore import Storage
from io import BytesIO
from flask import Flask
from PIL import Image
import base64
import json
import sys
import os

app = Flask(__name__)
storage = Storage()

def light(attendance, name , usn):
    fileName = "./images/"+usn+".png"
    ex = lightTheme("./manager/template.png", attendance = attendance , name=name)
    ex.loadPieCharts()
    ex.generateName()
    buffered = BytesIO()
    ex.getCompressed().save(buffered , format="PNG")
    ex.saveImage(fileName)
    x = base64.b64encode(buffered.getvalue())
    return x , fileName

def dark(attendance, name , usn):
    fileName = "./images/"+usn+".png"
    ex = darkTheme("./manager/darktemplate.png" , attendance = attendance , name=name)
    ex.loadPieCharts()
    ex.generateName()
    buffered = BytesIO()
    ex.getCompressed().save(buffered , format="PNG")
    ex.saveImage(fileName)
    x = base64.b64encode(buffered.getvalue())
    return x , fileName

@app.route("/rescrape/<usn>/<dob>")
def scrapeAndStore(usn , dob):
    usn = usn
    dob = dob
    stud = Scraper()
    stud.scrape(usn = usn ,dob =  dob)
    data = stud.getHTML()
    p = Parser(data)
    name , pp , courses , attendance = p.parse()
    attendanceTupleFormat = [(int(i) , 100-int(i) , sub) for i, sub in zip(attendance , courses)]
    b64Img , path = dark(attendanceTupleFormat , name , usn)
    storage.storeAttendance(usn , dob, name , courses , attendance , pp ,b64Img)
    url = storage.storeImage(path)
    return json.dumps({"message":"successs" , "url" : url})


if __name__ == '__main__':
   app.run(host="0.0.0.0" , port = int(os.environ.get('PORT' , 5000)))