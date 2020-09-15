from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from multiselectfield import MultiSelectField


GENRE = (('ACT', 'ACTION'),('ADV','ADVENTURE'),('COM','COMEDY'), ('CR','CRIME'), ('SCI-FY','SCI-FY') ,('ANI','ANIMATION'),('HOR','HORROR'), ('SH', 'SUPERHERO'), ('DR','DRAMA'))
STATUS = (('active', 'Active'), ('inactive', 'Inactive'), ('', 'Default'))
FIELDS = (('In Theatre 2020','In Theatre 2020'),('Coming Soon','Coming Soon'),('IMDB RATING','IMDB RATING'))
FIEL = (('POPULAR','POPULAR'),('Coming Soon','Coming Soon'),('RATING','IMDB RATING'))


class MajorItems(models.Model):
    Title = models.CharField(max_length=500)
    Image = models.ImageField(upload_to='media')
    Genre = MultiSelectField(choices=GENRE,default='basic')

    def __str__(self):
        return self.Title


class Movie(models.Model):
    Title = models.CharField(max_length=400)
    slug = models.CharField(max_length=500, unique=True)
    About = models.CharField(max_length=1000, default='Its Good')
    Video = models.TextField(max_length=500, default='Not Available')
    Image = models.ImageField(upload_to='media')
    Cast = models.TextField(max_length=1000, default='...')
    Rank = models.IntegerField(default='1')
    MoviesGenre = MultiSelectField(choices=GENRE)
    Field = models.CharField(max_length=200, choices=FIELDS, blank=False)
    Imdb_rating = models.CharField(max_length=200, blank=True, default='Not Yet Rated')
    Price = models.IntegerField()

    def __str__(self):
        return self.Title

    def get_movie_url(self):
        return reverse('home:movie', kwargs={
            'slug':self.slug
        })

    def add_to_cart(self):
        return reverse("home:add-to-cart", kwargs={
            'slug': self.slug
        })

    # def remove_from_cart_url(self):
    #     return reverse("core:remove-from-cart", kwargs={
    #         'slug': self.slug
    #     })

class OrderMovie(models.Model):
    ordered = models.BooleanField(default=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    checkout = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of { self.movie.Title}"

    def ticket_price(self):
        return self.quantity * self.movie.Price

    def final_price(self):
        return self.ticket_price()

    def remove_one_ticket(self):
        return reverse('home:removecart', kwargs={'slug': self.movie.slug})

    def remove_all_tickets(self):
        return reverse('home:deletecart', kwargs={'slug': self.movie.slug})

    def add_one_ticket(self):
        return reverse('home:add-to-cart', kwargs={'slug': self.movie.slug})


class Checkout(models.Model):
    Username = models.CharField(max_length=500)
    email = models.CharField(max_length=500)
    Address = models.CharField(max_length=500)
    City = models.CharField(max_length=500)
    State = models.CharField(max_length=500)
    Zip = models.CharField(max_length=500)
    NameOnCard = models.CharField(max_length=500)
    CCNumber = models.IntegerField()
    ExpDate = models.CharField(max_length=20)


    def __str__(self):
        return self.Username


class TotalCart(models.Model):
    movieitems = models.ManyToManyField(OrderMovie)
    checkout = models.BooleanField(default=False)
    cartname = models.CharField(max_length=20, default="admin")

    def __str__(self):
        return self.cartname

    def get_total(self):
        total = 0
        for x in self.movieitems.all():
            total += x.final_price()
        return total




class Tv(models.Model):
    Title = models.CharField(max_length=500)
    slug = models.CharField(max_length=500, unique=True, default=1)
    Image = models.ImageField(upload_to='media')
    About = models.CharField(max_length=1000, default='Its Good')
    Cast = models.TextField(max_length=1000, default='...')
    Rank = models.IntegerField()
    SeriesGenre = MultiSelectField(choices=GENRE)
    Field = models.CharField(max_length=200, choices=FIEL, blank=False, default=1)
    Imdb_rating = models.CharField(max_length=200, blank=True,default='Not Yet Rated')
    Price = models.IntegerField()

    def __str__(self):
        return self.Title

    def get_series_url(self):
        return reverse('home:series', kwargs={'slug': self.slug})

class Trailers(models.Model):
    Title = models.CharField(max_length=500)
    Image = models.ImageField(upload_to='media')
    Video = models.TextField(max_length=500)
    # Rank = models.IntegerField()
    # SeriesGenre = MultiSelectField(choices=GENRE)
    Length = models.TextField(max_length=200)

    def __str__(self):
        return self.Title




