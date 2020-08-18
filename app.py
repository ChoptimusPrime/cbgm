from flask import Flask, render_template, redirect, flash, g, request
from forms import LoginForm, RegisterForm
from models import User, db, connect_db
from secrets import FLASK_SECRET


app = Flask(__name__)

app.config['SECRET_KEY'] = FLASK_SECRET
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///cbgm_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def index():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User.register(username=form.username.data,
                                 password=form.password.data,
                                 email=form.email.data,
                                 first_name=form.first_name.data,
                                 last_name=form.last_name.data)
        if new_user:
            db.session.add(new_user)
            try:
                db.session.commit()
                flash(f" Welcome {new_user.username}")
                return redirect(request.url)
            except Exception as err:
                db.session.rollback()
                flash("Error connecting to database")
                return redirect(request.url)
    
    return render_template('register.html', form=form)