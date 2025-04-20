import http.client
import os
from dotenv import load_dotenv

load_dotenv("./.env")
conn = http.client.HTTPSConnection("concerts-artists-events-tracker.p.rapidapi.com")

print(os.getenv("RAPID_API_KEY") )
headers = {
    'x-rapidapi-key': os.getenv("RAPID_API_KEY"),
    'x-rapidapi-host': "concerts-artists-events-tracker.p.rapidapi.com"
}

conn.request("GET", "/location?name=Boise&minDate=2024-08-30&maxDate=2024-09-30&page=1", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))