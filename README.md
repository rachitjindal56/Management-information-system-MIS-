# Management-information-system-MIS-

This app is a Management Information System (MIS) which also has a login feature hashed feature to protect passwords. 
It's developed on Flask(python) for backend.
It uses 3 sqlite databases for storing the data

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///contacts.db" 
app.config['SQLALCHEMY_BINDS'] = {'login' : "sqlite:///login.db",
                                  'sheet' : "sqlite:///data.db"}

The database is having the following format:

class Contact(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(700), nullable=False)
    msg = db.Column(db.String(1000), nullable=False)
    
    
class Admin(db.Model, UserMixin):
    __bind_key__ = 'login'
    
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(300), nullable=True,unique=True)
    password = db.Column(db.String(200), nullable=False) 

class Sheet(db.Model):
    __bind_key__ = 'sheet'
    
    srno = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(300), nullable=True)
    password = db.Column(db.String(200), nullable=False)
    
The front-end is based on CSS and HTML. The app is deployed using Heroku using Procfile.
