from flask import Flask, render_template, request, redirect
import smtplib
import urllib2
from time import gmtime, strftime
import pymongo
import simplejson
from pymongo import Connection

connection = Connection('localhost', 27017)
db = connection.commits
collection = db.commits
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    email = request.json["email"]
    message = request.json["message"]

    url = "https://api.github.com/legacy/user/email/"+email
    f = urllib2.urlopen(url)
    response = f.read()
    f.close()
    response = simplejson.loads(response)

    realname = response['user']['name']
    username = response['user']['login']
    time = strftime("%d-%m-%Y %H:%M:%S")
    picture = "http://www.gravatar.com/avatar/"+response['user']['gravatar_id']
    commitId = message

    collection.insert({ "username":username, "realname":realname, "email":email, "picture":picture, "message":message, "commitId":commitId, "time":time })

    return ""
  else:
    commits = collection.find({})
    return render_template('index.html', commits=commits)

if __name__ == '__main__':
  app.run("akenn.org", 9000)
