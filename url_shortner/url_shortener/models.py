from datetime import datetime
from random import choices
from .extensions import db
import string


class Link(db.Model):
    # creating columns in our database in order to store data
    # id is generated by the database
    id = db.Column(db.Integer, primary_key=True)
    # this is what we are passing into our class
    original_url = db.Column(db.String(512))
    # defaults to the generate function
    short_url = db.Column(db.String(3), unique=True)
    # every time someone uses a link, need to record
    visits = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now)

    # kwargs are just dictionary key/value pairs that go together with the variables in the
    # called function
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_link()

    def generate_short_link(self):
        # string.digits returns a constant '123456789'
        # string.ascii_letters returns all upper and lowercase ascii letters
        characters = string.digits + string.ascii_letters
        print('character: ' + characters)
        # this is going to join together 3 random sets of characters.
        short_url = ''.join(choices(characters, k=3))
        print('short_url: ' + short_url)

        # check to see if the short_url already exists within the database
        link = self.query.filter_by(short_url=short_url).first()

        if link:
            return self.generate_short_link()

        return short_url


