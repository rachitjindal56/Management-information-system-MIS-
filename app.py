from flask import Flask, render_template, redirect, request, url_for
from form import Login, Register, Registrationform
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, UserMixin, logout_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///contacts.db"
app.config['SQLALCHEMY_BINDS'] = {'login' : "sqlite:///login.db",
                                  'sheet' : "sqlite:///data.db"}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '33c062ea7be6d2190072ca056353edfa'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


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
        

@app.route("/",methods=['POST','GET'])
def home():
    if request.method == "POST":
        email = request.form['email']
        name = request.form['name']
        phone = request.form['phone']
        msg = request.form['message']
        
        details = Contact(email=email,phone=phone,name=name,msg=msg)
        db.session.add(details)
        db.session.commit()
        
    return render_template("home.html")

@app.route("/about")
def info():    
    return render_template("about.html")

@app.route("/contact",methods=['POST','GET'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        msg = request.form['message']
        
        detail = Contact(email=email,name=name,msg=msg,phone=phone)
        db.session.add(detail)
        db.session.commit()
        return redirect("/")
        
    return render_template("contact.html")

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

@app.route("/login",methods=['POST','GET'])
def login():
    form = Login()
    
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first() 
        if user:
            if bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user)
                return redirect(url_for("dashboard"))
        
    return render_template("login.html",form=form)

@app.route("/register",methods=['POST','GET'])
def register():
    form = Register()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = Admin(username=form.username.data,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
        
    return render_template("register.html",form=form)

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("data.html")

@app.route("/sheet")
@login_required
def sheet():
    data = Sheet.query.all()
    return render_template("/sheet.html",data=data)


@app.route("/delete/<int:srno>")
@login_required
def delete(srno):
    query = Sheet.query.filter_by(srno=srno).first()
    db.session.delete(query)
    db.session.commit()
    return redirect(url_for('sheet'))

@app.route("/update/<int:srno>",methods=['POST','GET'])
@login_required
def update(srno):
    form = Registrationform()
    
    if form.validate_on_submit():
        data = Sheet.query.filter_by(srno=srno).first()
        data.email = form.username.data
        data.password = form.password.data
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('sheet'))
    
    query = Sheet.query.filter_by(srno=srno).first()
    return render_template('update.html',dx=query,form=form)    

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)