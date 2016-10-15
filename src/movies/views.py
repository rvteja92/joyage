from django.shortcuts import render
from django.core.paginator import Paginator

from .models import Movie, Show


def home(request):
    page_no = int(request.GET.get('page', '1'))
    all_movies  = Movie.objects.all()
    pages   = Paginator(all_movies, 12)
    return render(request, 'movies/index.html',
        {
            'page': pages.page(page_no),
            'number': pages.num_pages
        })

def movie(request, movie_id):
    movie   = Movie.objects.get(id=movie_id)
    shows   = Show.objects.filter(movie=movie)

    # Using python dictionaries to aggregate show times of theaters
    show_times   = {}
    for show in shows:
        if show.theater in show_times:
            show_times[show.theater] += [show.time.strftime('%I:%M %p'),]
        else:
            show_times[show.theater] = [show.time.strftime('%I:%M %p'),]

    # As dictionaries cannot be paginated, it is converted to list of lists
    show_list = []
    for theater, shows in show_times.items():
        show_list += [[theater.name, theater.address, shows]]

    page_no = int(request.GET.get('page', '1'))
    show_pages   = Paginator(show_list, 10)

    return render(request, 'movies/shows.html',
        {
            'movie': movie,
            'shows': show_pages.page(page_no),
            'number': show_pages.num_pages
        })
