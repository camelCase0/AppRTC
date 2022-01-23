from flask_login import UserMixin

from project import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    creator = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return '<Room %r>' % self.id

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))