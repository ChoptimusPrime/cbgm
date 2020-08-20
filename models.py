from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):

    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    cards = db.relationship("Card", backref="user", order_by="Card.year.desc()")

    @classmethod
    def register(cls, username, password, email, first_name, last_name):

        hashed = bcrypt.generate_password_hash(password)
        pwd_utf8 = hashed.decode("utf8")

        return cls(username=username,
                   password=pwd_utf8,
                   email=email,
                   first_name=first_name,
                   last_name=last_name)

    @classmethod
    def authenticate_user(cls, username, password):

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class Card(db.Model):

    __tablename__ = "cards"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='cascade'), nullable=False)
    player = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    set_name = db.Column(db.Text, nullable=False)
    number = db.Column(db.Text)
    parallel = db.Column(db.Boolean, default=False)
    img_url = db.Column(db.Text, default=None)

    def serialize(self):
        return {'player'   : self.player,
                'year'     : self.year,
                'set_name' : self.set_name,
                'number'   : self.number,
                'parallel' : self.parallel}

    def get_string_info(self):
        return f"{self.year} {self.set_name} {self.number} {self.player}"