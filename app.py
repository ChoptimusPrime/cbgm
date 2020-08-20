from flask import Flask, render_template, redirect, flash, g, request, session
from forms import LoginForm, RegisterForm, CardForm
from models import User, db, connect_db, Card
from constants import S3, AWS_BUCKET
from secrets import FLASK_SECRET

USER_KEY = 'user_key'


app = Flask(__name__)

app.config['SECRET_KEY'] = FLASK_SECRET
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///cbgm_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.before_request
def add_user_to_g():

    if USER_KEY in session:
        g.user = User.query.get(session[USER_KEY])
    else:
        g.user = None

@app.route('/')
def index():
    if g.user:
        return redirect(f'/users/{g.user.id}')
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
                session[USER_KEY] = new_user.id
                flash(f" Welcome {new_user.username}")
                return redirect(f'users/{new_user.id}')
            except Exception as err:
                db.session.rollback()
                print(err)
                flash("Error connecting to database")
                return redirect(request.url)
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate_user(username=form.username.data, password=form.password.data)
        if user:
            session[USER_KEY] = user.id
            flash("Authenticated!")
            return redirect(f"/users/{user.id}")
        else:
            flash("Username or password incorrect")
            return redirect("/login")
    return render_template("login.html", form=form)

@app.route('/users')
def all_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/<int:user_id>')
def show_user(user_id):
    if not g.user:
        flash("You must log in for access")
        return redirect('/login')
    user = User.query.get(user_id)
    return render_template('user.html', user=user)

@app.route('/users/<int:user_id>/add_card', methods=["GET", "POST"])
def add_card(user_id):
    if not g.user:
        flash("You must be logged in for access")
        return redirect("/register")
    elif g.user.id != user_id:
        flash("You can only add to your collection")
        return redirect(f"/users/{g.user.id}")
    else:
        form = CardForm()
        if form.validate_on_submit():
            new_card = Card(owner_id=user_id, 
                            player=form.player.data, 
                            year=form.year.data, 
                            set_name=form.set_name.data, 
                            number=form.number.data, 
                            parallel=form.parallel.data)
            db.session.add(new_card)
            try:
                db.session.commit()
                if form.img.data:
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    img_data = request.files[form.img.name].read()
                    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                    print(img_data)
                    file_key = f"card_images/{g.user.id}/{new_card.id}.jpg"
                    response = S3.put_object(Body=img_data, Bucket=AWS_BUCKET, Key=file_key, ACL="public-read")
                    print(response)
                    img_url = f"https://cardboardgmpics.s3-us-west-2.amazonaws.com/{file_key}"
                    new_card.img_url = img_url
                    db.session.commit()
                flash("Card successfully added")
                return redirect(request.url)
            except Exception as err:
                db.session.rollback()
                flash("Error adding card")
                return redirect(request.url)
        return render_template("add-card.html", form=form)

@app.route('/logout', methods=['POST'])
def logout_user():

    session.pop(USER_KEY)
    flash("You have logged out!")
    return redirect("/login")




