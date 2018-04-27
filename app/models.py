from . import db


class UserProfile(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    gender = db.Column(db.String(10))
    email = db.Column(db.String(255))
    location = db.Column(db.String(100))
    biography = db.Column(db.String(255))
    pic = db.Column(db.String(80))
    created_on = db.Column(db.String(20))
    

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.first_name)
