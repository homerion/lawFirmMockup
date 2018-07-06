from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    first_name=db.Column(db.String(100))
    last_name=db.Column(db.String(100))
    username=db.Column(db.String(16),index=True, unique=True)
    email=db.Column(db.String(120),index=True, unique=True)
    password_hash=db.Column(db.String(256))
    # role=db.relationship('User_Role', backref='user',lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return 'Username= {}, Email = {}'.format(
        self.username,self.email)

class Role(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(48), unique=True)
    description=db.Column(db.String(5000))

    def __repr__(self):
        return '{}: {}'.format(
        self.name,self.description)

class User_Role(db.Model):
    relation_id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    role_id=db.Column(db.Integer,db.ForeignKey('role.id'))

Roles_Table = db.Table('User_to_Role', db.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
