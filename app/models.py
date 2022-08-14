from app import db , bcrypt , login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email = db.Column(db.String(length=100), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    items = db.relationship('Task', backref='task_creator', lazy=True)


    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')


    def check_password(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash , attempted_password)

    def __repr__(self):
        return f"{self.username} "




class Task(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(length=1000), nullable=False )
    is_completed = db.Column(db.Boolean(), default=False, nullable=False)
    created_date = db.Column(db.DateTime(), default=datetime.utcnow)
    creator = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f"{self.description}"

