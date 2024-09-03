from showSearcher import showSearcher
from datetime import date, timedelta

searcher = showSearcher()

data = searcher.retrieveShows("Boise", date.today(), date.today() + timedelta(days = 14))

print(data)
