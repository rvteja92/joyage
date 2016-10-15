import requests
import json
import os.path
from functools import reduce
import datetime
import re
import traceback

from django.core.management.base import BaseCommand, CommandError
from django.core import management

from ...models import Movie, Theater, Tag, Show


class Command(BaseCommand):
    data    = None
    movies  = {}
    movie_objects = {}
    theaters    = {}
    theater_objects = {}
    tags    = {}
    tag_objects = {}
    # shows   = {}

    def handle(self, *args, **options):
        if not self.check_data_file():
            print('Cannot get data\nExiting')
            return
        print('Data found...\nFlushing old data...')
        management.call_command('flush', verbosity=0, interactive=False)
        if self.load_data():
            print('Data successfully written to database')
        else:
            print('Data could not be committed to database')

    def load_data(self):
        for theater in self.data:
            for movie in theater['movies']:
                for tag in movie['tags']:
                    if tag:
                        self.tags[tag.strip()]  = tag.strip()
        for tag in self.tags:
            Tag.objects.create(name=tag)

        print('All tags created successfully')

        for theater in self.data:
            for movie in theater['movies']:
                self.movies[movie['name'].strip()] = movie

        for name, movie in self.movies.items():
            m = Movie.objects.create(name=movie['name'].strip(),
                            image=movie['image'],
                            screen_format=movie['screen_format'].strip() if movie['screen_format'] else 'Info Not Available',
                            duration=reduce(lambda h, m: int(h)*60 + int(m), re.match(r'([0-9]+) hr ([0-9]+) min', movie['duration']).groups() if re.match(r'([0-9]+) hr ([0-9]+) min', movie['duration']) else (0, 0,))
                            )

            for tag in movie['tags']:
                if tag:
                    m.tags.add(Tag.objects.get(name=tag.strip()))

        print('All movies tagged successfully')

        for theater in self.data:
            self.theaters[theater['theater_name'].strip()] = theater

        for name, theater in self.theaters.items():
            t = Theater.objects.create(
                name    = theater['theater_name'].strip(),
                city    = theater['city'],
                address = theater['address'],
                page    = theater['theater_link']
            )

        print('All theaters created successfully')

        for theater in self.data:
            for movie in theater['movies']:
                for time in movie['timings_link']:
                    show    = Show.objects.create(
                        movie   = Movie.objects.get(name=movie['name'].strip()),
                        theater = Theater.objects.get(name=theater['theater_name'].strip()),
                        time = datetime.datetime.strptime(time['time'].strip(), '%I:%M%p').time()
                    )
        print('All shows registered successfully')
        return True

    def check_data_file(self):
        print('Looking for "movie_data.json" file...')
        if os.path.isfile('movie_data.json'):
            with open('movie_data.json') as datafile:
                try:
                    self.data = json.load(datafile)
                    return True
                except ValueError as ve:
                    print('Invalid file data')

        print('Downloading movie data...')
        try:
            r   = requests.get('http://188.166.208.228/us_movies/', timeout=2)

        except requests.ConnectionError:
            print('Cannot connect to internet.')
            return False

        with open('movie_data.json', 'w') as datafile:
            json.dump(r.json(), datafile, indent=4,)
            return True
