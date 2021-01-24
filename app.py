##########################################
# Steps to take before running the script#
##########################################
# 1. pip install virtualenv -  needed to create an isolated environment
# 2. python -m venv virtual - this creates a folder called "virtual" in which\
# you can find all the files needed for the virtual environment 
# 3. .\virtual\Scripts\activate - activates the virtual environment;\
# commands will be run in this environment untile deactivation
# 4. pip install flask

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_email
from sqlalchemy.sql import func

app=Flask(__name__)   # "__name__" is a placeholder;\
                      # here you enter the name of the script that runs the app.
                      # below there is a statement "if __name__=='__main__'";\
                      # "__main__" refers to the current script
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres123@localhost/height_collector'
db=SQLAlchemy(app)

#>>> from app import db
#>>> db.create_all()

class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    height_=db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email_=email_
        self.height_=height_


@app.route("/")     # when calling the homepage(index.html) this function will be executed
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])  # the implicit method is "GET";\ 
                                          # other methods, like "POST", need to be specified 
def success():
    if request.method=='POST':                # the function process' only "POST" requests 
        email=request.form["email_name"]      # syntax for capturing value sent to the webserver
        height=request.form["height_name"]
        # print(email, height)
        
        # print(request.form)
        # print(db.session.query(Data).filter(Data.email_==email).count())  # checks if the email address is already in the database;\
                                                                           # if the result is "0" the email is not in the database
        # "pip install psycopg2" + "pip install Flask-SQLAlchemy"\
        # in order to access the PostreSQL database
        if db.session.query(Data).filter(Data.email_==email).count() == 0: # if the email is not in the data base it adds is
            data=Data(email,height)
            db.session.add(data)
            db.session.commit()
            average_height=db.session.query(func.avg(Data.height_)).scalar()
            average_height=round(average_height)
            count=db.session.query(Data.height_).count()
            send_email(email, height, average_height, count)
            #print(average_height)
            return render_template("success.html")  
    # if the email is in the data base it returns to the homepage
    return render_template("index.html",
    text="Seems like we've got something from that email address already!")               
    


if __name__=='__main__':   # "__main__" means the script in which we are now is to be executed not another imported script
    app.debug=True
    app.run()              # within the brackets you can specify the port (port=5001);\
                           # otherwise standard port 5000 will be used
