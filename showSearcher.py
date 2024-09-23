import sqlite3
import http.client
import os
from dotenv import load_dotenv
from datetime import date
import json

class showSearcher(object):
    def __init__(self) -> None:
        load_dotenv()
        self.dbCon = sqlite3.connect("shows.db")
        self.showAPI = http.client.HTTPSConnection("concerts-artists-events-tracker.p.rapidapi.com")
        self.headers = {
            'x-rapidapi-key': os.getenv("RAPID_API_KEY"),
            'x-rapidapi-host': "concerts-artists-events-tracker.p.rapidapi.com"
        }

    def queryConcertApi(self, city, start, end, page=1):
        print("Hitting API")
        request = f'/location?name={city}&minDate={start}&maxDate={end}&page={page}'
        self.showAPI.request("GET", request, headers=self.headers)
        res = self.showAPI.getresponse()
        data = res.read()
        showData = data.decode("utf-8")
        json_data = json.loads(showData)

        result = []
        for record in json_data['data']:
            for artist in record['performer']:
                try:
                    self.dbCon.execute('''insert into shows (city, show_date, venue, venue_same_as, concert_id, artist_name, artist_id, image) 
                                        Values (?, ?, ?, ?, ?, ?, ?, ?)''',
                                        (
                                            city,
                                            str(record['startDate']).split('T')[0],
                                            record['location']['name'],
                                            record['location']['sameAs'],
                                            record['concert_id'],
                                            artist['name'],
                                            artist['artist_id'],
                                            record['image']
                                            )
                                        )
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
        previosSearch = self.dbCon.execute("select * from searches where city='%s' AND start_date='%s' AND end_date='%s'" % (city, start, end)).fetchone()
        #TODO: Check if date range overlaps with previous search, take all the shows in that range, start on specific page based on number of results

        if previosSearch != None: 
            searchResponse = self.dbCon.execute("select * from shows where city='%s' AND date(show_date) BETWEEN '%s' AND '%s'" % (city, start, end)).fetchall()
            return searchResponse
        

        page = 1
        result = self.queryConcertApi(city, start, end, page)

        while len(result)%50 == 0:
            page += 1
            result.extend(self.queryConcertApi(city, start, end, page))
                
        self.dbCon.execute("insert into searches (city, date_updated, start_date, end_date) VALUES (?, ?, ?, ?)", (city, str(date.today()), start, end))
        self.dbCon.commit()

        return result
        
    



        



