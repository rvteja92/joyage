from django.db import models


class Tag(models.Model):
    name    = models.CharField(max_length=40)

    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    name    = models.CharField(max_length=256)
    tags    = models.ManyToManyField(Tag)
    image   = models.CharField(max_length=256)
    screen_format   = models.CharField(max_length=256, default="Information Not Available")
    duration    = models.PositiveIntegerField() # Movie run time in minutes

    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

    def get_duration(self):
        hrs = self.duration // 60
        mins    = self.duration % 60
        return str(hrs) + ' hr ' + str(mins) + ' min'

class Theater(models.Model):
    name    = models.CharField(max_length=256)
    city    = models.CharField(max_length=4)
    address = models.CharField(max_length=256)
    page    = models.CharField(max_length=256)  # Theatre link (page)
    movies  = models.ManyToManyField(Movie, through='Show')

    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name


class Show(models.Model):
    theater = models.ForeignKey(Theater)
    movie   = models.ForeignKey(Movie)
    time    = models.TimeField()

    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return '"' + str(self.movie) + '" in ' + str(self.theater) + ', at ' + str(self.time)

    def get_timing(self):
        return self.time.strftime('%I:%M %p')
