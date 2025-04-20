import http.client
import os
from app import app
from dotenv import load_dotenv
from datetime import date
import json
from app.models import Searches, Shows, ShowsSchema, UserShows, UserShowsSchema
import sqlalchemy as sa
from sqlalchemy.orm import Session

class showSearcherAlchemy(object):
    def __init__(self) -> None:
        load_dotenv()
        self.showAPI = http.client.HTTPSConnection("concerts-artists-events-tracker.p.rapidapi.com")
        self.headers = {
            'x-rapidapi-key': os.getenv("RAPID_API_KEY"),
            'x-rapidapi-host': "concerts-artists-events-tracker.p.rapidapi.com"
        }

    def queryConcertApi(self, city, start, end, page=1):
        request = f'/location?name={city}&minDate={start}&maxDate={end}&page={page}'
        self.showAPI.request("GET", request, headers=self.headers)
        res = self.showAPI.getresponse()
        data = res.read()
        showData = data.decode("utf-8")
        json_data = json.loads(showData)
        engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

        result = []
        for record in json_data['data']:
            for artist in record['performer']:
                try:
                    with Session(engine) as session:    
                        insertQuery = sa.insert(Shows).values(
                            city = city,
                            show_date=str(record['startDate']).split('T')[0] , 
                            venue=record['location']['name'], 
                            venue_same_as=record['location']['sameAs'], 
                            concert_id=record['concert_id'], 
                            artist_name=artist['name'], 
                            artist_id=artist['artist_id'], 
                            image=record['image']
                            )
                        session.execute(insertQuery)
                        session.commit()
                except:
                    continue


        result.append({
                'city': city,
                'show_date': str(record['startDate']).split('T')[0],
                'venue': record['location']['name'] if 'name' in record['location'].keys() else '', 
                'venue_same_as': record['location']['sameAs'] if 'sameAs' in record['location'].keys() else '',
                'concert_id' : record['concert_id'],
                'artist_name' : artist['name'],
                'artist_id' : artist['artist_id'],
                'image' : record['image']
                })
        
        
        return result

        

    def retrieveShows(self, city, start, end):
        engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        with Session(engine) as session:
            query = sa.select(Searches).where(Searches.city == city, Searches.start_date == start, Searches.end_date == end)
            previosSearch = session.execute(query).fetchone()
        
            if previosSearch != None: 
                showSearchQuery = sa.select(Shows).where(Shows.city == city, Shows.show_date >= start, Shows.show_date <= end)
                showSearcherResponse = session.scalars(showSearchQuery)
                shows_schema = ShowsSchema(many=True)

                resShows = shows_schema.dump(showSearcherResponse)
                print('DATABASE shows')
                return resShows
        

            page = 1
            result = self.queryConcertApi(city, start, end, page)

            while len(result)%50 == 0:
                page += 1
                result.extend(self.queryConcertApi(city, start, end, page))
                    

            insertQuery = sa.insert(Searches).values(city = city, date_updated=str(date.today()), start_date = start, end_date=end)
            session.execute(insertQuery)
            session.commit()

            return result
    
    def saveShow(self, user_id, show_id):
        engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        with Session(engine) as session:
            insertQuery = sa.insert(UserShows).values(user_id = user_id, show_id=show_id)
            try:
                session.execute(insertQuery)
                session.commit()
                return('success')
            except:
                return ('failed')
            
    def removeShow(self, user_id, show_id):
        engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        with Session(engine) as session:
            deleteQuery = sa.delete(UserShows).filter(UserShows.show_id == show_id, UserShows.user_id==user_id)
            try:
                session.execute(deleteQuery)
                session.commit()
                return('success')
            except:
                return ('failed')
            
    def getUserShows(self, user_id):
        engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        with Session(engine) as session:
            query = sa.select(UserShows).where(UserShows.user_id == user_id)
            userShows = session.scalars(query)

            userShowsSchema = UserShowsSchema(many=True)
            userShowsResult = userShowsSchema.dump(userShows)
            userShowsResultArray = []

            for x in userShowsResult:
                userShowsResultArray.append(x['show_id'])

            return userShowsResultArray

    def saveSpotifyID(self, concert_id, artist_id, artist_spotify_id):
        engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        with Session(engine) as session:
            showQuery = sa.select(Shows).where(Shows.concert_id == concert_id, Shows.artist_id == artist_id)
            try:
                show = session.scalars(showQuery).one()
                show.artist_spotify_id = artist_spotify_id
                session.commit()
                return('success')
            except Exception as e:
                print(e)
                return ('failed')
    
    def getSpotifyIDs(self, concert_id):
        engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        with Session(engine) as session:
            query = sa.select(Shows).where(Shows.concert_id == concert_id)
            showsResultArray = []
            try:
                shows = session.scalars(query)

                showsSchema = ShowsSchema(many=True)
                showsResult = showsSchema.dump(shows)
                

                for x in showsResult:
                    showsResultArray.append(x['artist_spotify_id'])
            
            except Exception as e:
                print('Exception')
                print(e)
                return 'failed'

            return showsResultArray

        



