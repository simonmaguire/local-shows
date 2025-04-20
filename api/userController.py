
from app import app
from dotenv import load_dotenv
import json
from app.models import  User
import sqlalchemy as sa
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


def saveProfile(profile):
        engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        with Session(engine) as session:
            insertQuery = sa.insert(User).values(
                spotify_id = int(profile['spotify_id']),
                username=profile['username'],
                email = profile['email'],
                product=profile['product'],
                country=profile['country']
            )
            try:
                session.execute(insertQuery)
                session.commit()
            except IntegrityError:
                 session.rollback()
