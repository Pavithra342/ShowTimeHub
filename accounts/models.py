from django.db import models
from django.contrib.auth.models import User

class Cinema(models.Model):
    cinema = models.AutoField(primary_key=True)
    role = models.CharField(max_length=30, default='cinema_manager')
    cinema_name = models.CharField(max_length=50)
    phoneno = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.cinema_name
        
class Movie(models.Model):
    movie = models.AutoField(primary_key=True)
    movie_name = models.CharField(max_length=255)
    movie_des = models.TextField()
    movie_genre = models.CharField(max_length=100)
    movie_duration = models.CharField(max_length=10)
    movie_rating = models.FloatField()
    movie_rdate = models.DateField()
    movie_poster = models.ImageField(upload_to='posters/')
    movie_trailer = models.URLField()

    def __str__(self):
        return self.movie_name

class Shows(models.Model):
    shows = models.AutoField(primary_key=True)
    cinema = models.ForeignKey('Cinema', on_delete=models.CASCADE, related_name='cinema_show')
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='movie_show')
    time = models.CharField(max_length=100)
    date = models.CharField(max_length=15, default="")
    price = models.IntegerField()

    def __str__(self):
        return f"{self.cinema.cinema_name} | {self.movie.movie_name} | {self.time}"

class Bookings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shows = models.ForeignKey(Shows, on_delete=models.CASCADE)
    useat = models.CharField(max_length=100)

    @property
    def useat_as_list(self):
        return self.useat.split(',')

    def __str__(self):
        return f"{self.user.username} | {self.shows.movie.movie_name} | {self.useat}"
