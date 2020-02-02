from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import base64


class Scraper: 
  def randString(self,n):
    return "l"*n
  def check(self,usn):
    password = usn
    rand = ''
    for i in password:
      rand += i+self.randString(2)
    encoded = base64.b64encode(rand.encode())
    return encoded
  def scrape(self , usn , dob):
    self.browser = RoboBrowser(history = False , parser='html.parser')
    self.browser.open('http://parents.msrit.edu/index.php' )
    form = self.browser.get_forms()[0]
    form['username'].value = usn
    form['password'].value = self.check(dob)
    form['passwd'].value = self.check(dob)
    self.browser.submit_form(form)
  def getHTML(self):
    """
    returns parsed HTML
    """
    return str(self.browser.parsed)


class Parser:
  def __init__(self , data):
    self.data = data
  def parse(self):
    """
    returns : (img_src , [cournames] , [attendance])
    """
    soup = BeautifulSoup(self.data,"html.parser")
    coursename = soup.find_all("div" , {"class":"coursename"})
    coursename = [i.text for i in coursename]
    attendance = soup.find_all("a" , {"title":"Attendence"})
    imgsrc = soup.find("img" , {"class":"imagize"})
    imgsrc = "http://parents.msrit.edu/"+imgsrc['src']
    attendance = [i.text[:-1] for i in attendance if i.text!="Attendance"]
    name = soup.find("div" , {"class":"tname2"}).text
    name = name.strip()
    return (name ,imgsrc ,coursename ,  attendance)



