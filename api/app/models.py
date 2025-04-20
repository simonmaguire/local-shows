from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db, ma
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
import jwt
import time


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    spotify_id: so.Mapped[int] = so.mapped_column(nullable=False, unique=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    product: so.Mapped[str] = so.mapped_column(sa.String(32))
    country: so.Mapped[str] = so.mapped_column(sa.String(16))
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_auth_token(self, expiration = 600):
        return jwt.encode({'id': self.id, 'exp': time.time() + expiration}, app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],
                              algorithms=['HS256'])
        except:
            return
        return User.query.get(data['id'])
    
class Artist(db.Model):
    artist_spotify_id: so.Mapped[str] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128))
    image: so.Mapped[str] = so.mapped_column(sa.String(256), nullable=True)


class Shows(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    city: so.Mapped[str] = so.mapped_column(sa.String(64))
    show_date: so.Mapped[str] = so.mapped_column(sa.String(15))
    venue: so.Mapped[str] = so.mapped_column(sa.String(64))
    venue_same_as: so.Mapped[str] = so.mapped_column(sa.String(256))
    concert_id: so.Mapped[str] = so.mapped_column(sa.String(64))
    artist_name: so.Mapped[str] = so.mapped_column(sa.String(64))
    artist_id: so.Mapped[str] = so.mapped_column(sa.String(64))
    artist_spotify_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey(Artist.artist_spotify_id), index=True, nullable=True)
    image: so.Mapped[str] = so.mapped_column(sa.String(256))
    __table_args__ = (sa.UniqueConstraint(city, show_date, artist_name, name="unique_shows"),)

    def __repr__(self):
        return '<Show {} in {} on {}>'.format(self.artist_name, self.city, self.show_date)
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    


class UserShows(db.Model):
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.spotify_id), primary_key=True,  index=True)
    show_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Shows.concert_id), primary_key=True,  index=True)

    def __repr__(self):
        return '<UserShow {} saved {}>'.format(self.user_id, self.show_id)
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Searches(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    city: so.Mapped[str] = so.mapped_column(sa.String(64))
    start_date: so.Mapped[str] = so.mapped_column(sa.String(15))
    end_date: so.Mapped[str] = so.mapped_column(sa.String(15))
    date_updated : so.Mapped[str] = so.mapped_column(sa.String(15)) 
    __table_args__ = (sa.UniqueConstraint(city, start_date, end_date, name="unique_searches"),)

    def __repr__(self):
        return '<Search City: {} between {} and {} >'.format(self.city, self.start_date, self.end_date)

class ShowsSchema(SQLAlchemySchema):
    class Meta:
        model = Shows
        load_instance=True

    id = auto_field()
    city = auto_field()
    show_date = auto_field()
    venue = auto_field()
    venue_same_as = auto_field()
    concert_id = auto_field()
    artist_name = auto_field()
    artist_id = auto_field()
    image = auto_field()
    artist_spotify_id = auto_field()

class UserShowsSchema(SQLAlchemySchema):
    class Meta:
        model = UserShows
        load_instance = True
    
    user_id = auto_field()
    show_id = auto_field()