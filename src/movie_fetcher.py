import re
import csv
import requests
from bs4 import BeautifulSoup

class AccesoImdb:
    def __init__(self, url):
        self.url = url
        
    def get_top_movies(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'lxml')

        movies = soup.select('td.titleColumn')
        links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
        crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
        ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
        votes = [b.attrs.get('data-value') for b in soup.select('td.ratingColumn strong')]

        list = []

        for index in range(0, len(movies)):
            movie_string = movies[index].get_text()
            movie = (' '.join(movie_string.split()).replace('.', ''))
            movie_title = movie[len(str(index)) + 1:-7]
            year = re.search('\((.*?)\)', movie_string).group(1)
            place = movie[:len(str(index)) - (len(movie))]

            data = {"movie_title": movie_title,
                    "year": year,
                    "place": place,
                    "star_cast": crew[index],
                    "rating": ratings[index],
                    "vote": votes[index],
                    "link": links[index],
                    "preference_key": index % 4 + 1}
            list.append(data)
        return list

class Peli:
    def __init__(self, filename):
        self.filename = filename
        
    def write_to_csv(self, data):
        fields = ["preference_key", "movie_title", "star_cast", "rating", "year", "place", "vote", "link"]
        with open(self.filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            for movie in data:
                writer.writerow({**movie})

def main():
    url = 'http://www.imdb.com/chart/top'
    imdb_acceso = AccesoImdb(url)
    movie_data = imdb_acceso.get_top_movies()
    
    writer = Peli("movie_results.csv")
    writer.write_to_csv(movie_data)

if __name__ == '__main__':
    main()