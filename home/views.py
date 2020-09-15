from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
import django_filters
from django.urls import path
from .forms import CheckoutForm

from django.views.generic import ListView, DetailView, View
from .models import Movie, Tv, OrderMovie, TotalCart, Checkout, MajorItems, Trailers

class BaseView(View):
    view = {}

class HomeView(BaseView):
    def get(self,request):
        self.view['TapeT'] = MajorItems.objects.all()
        self.view['Hall1'] = Movie.objects.filter(Rank=1)
        self.view['Hall2'] = Movie.objects.filter(Rank=2)
        self.view['Hall3'] = Movie.objects.filter(Rank=3)
        self.view['TV1'] = Tv.objects.filter(Rank=1)
        self.view['TV2'] = Tv.objects.filter(Rank=2)
        self.view['TV3'] = Tv.objects.filter(Rank=3)
        self.view['Demo'] = Trailers.objects.all()
        return render(self.request,'index.html',self.view)


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'moviesingle.html'


class SeriesDetailView(DetailView):
    model = Tv
    template_name = 'seriessingle.html'



class MovieGenre(BaseView):
    def get(self,request):
        self.view['Genre1'] = Movie.objects.filter(MoviesGenre__contains = 'SH')
        self.view['Genre2'] = Movie.objects.filter(MoviesGenre__contains='ACT')
        self.view['Genre3'] = Movie.objects.filter(MoviesGenre__contains='COM')
        self.view['Genre4'] = Movie.objects.filter(MoviesGenre__contains='SCI-FY')
        self.view['Genre5'] = Movie.objects.filter(MoviesGenre__contains='ANI')
        self.view['Genre6'] = Movie.objects.filter(MoviesGenre__contains='DR')
        self.view['Genre7'] = Movie.objects.filter(MoviesGenre__contains='HOR')
        self.view['Genre8'] = Movie.objects.filter(MoviesGenre__contains='ADV')
        return render(self.request, 'MovieGenre.html', self.view)

class TvGenre(BaseView):
    def get(self,request):
        self.view['Genre1'] = Tv.objects.filter(SeriesGenre__contains='SH')
        self.view['Genre2'] = Tv.objects.filter(SeriesGenre__contains='ACT')
        self.view['Genre3'] = Tv.objects.filter(SeriesGenre__contains='COM')
        self.view['Genre4'] = Tv.objects.filter(SeriesGenre__contains='SCI-FY')
        self.view['Genre5'] = Tv.objects.filter(SeriesGenre__contains='ANI')
        self.view['Genre6'] = Tv.objects.filter(SeriesGenre__contains='DR')
        self.view['Genre7'] = Tv.objects.filter(SeriesGenre__contains='HOR')
        self.view['Genre8'] = Tv.objects.filter(SeriesGenre__contains='ADV')
        return render(self.request,'TvGenre.html', self.view)

class SearchViewMovies(BaseView):
    def get(self,request):
        query = request.GET.get('query',None)
        if not query:
            return redirect('/')

        self.view['search_Movie'] = Movie.objects.filter(Title__icontains = query)
        return render(request,'searchMovies.html',self.view)

class SearchViewSeries(BaseView):
    def get(self,request):
        query = request.GET.get('query',None)
        if not query:
            return redirect('/')

        self.view['search_Series'] = Tv.objects.filter(Title__icontains = query)
        return render(request,'searchSeries.html',self.view)

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['password1']

        if password == cpassword:
            if User.objects.filter(username = username).exists():
                messages.error(request,'Username is already taken')
                return render(request, 'register.html')
            elif User.objects.filter(email = email).exists():
                messages.error(request,'This email has already been used to create account.')
                return render(request, 'register.html')
            else:
                user = User.objects.create_user(
                    username = username,
                    email = email,
                    password = password
                 )
                TotalCart.cartname = user.username
                TotalCart.cartname.update()
                user.save()
                messages.success(request,'You have been successfully registered.')
                return render(request, 'register.html')
        else:
                messages.error(request,'Password does not match.')
                return render(request, 'register.html')

    return render(request, 'register.html')

class OrderView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            totalcart = TotalCart.objects.get(checkout=False)
            context = {
                'object': totalcart
            }
            # user = User.objects.all()
            # TotalCart.cartname = User.objects.get.username
            return render(self.request,"cart.html",context)
        except ObjectDoesNotExist:
            messages.error(self.request, "No movie in your cart.")
            return render(self.request,'/')


@login_required
def add_to_cart(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    order_movie, created = OrderMovie.objects.get_or_create(movie=movie,
    checkout= False
    )
    totalcart_qs = TotalCart.objects.filter(checkout= False)
    if totalcart_qs.exists():
        totalcart = totalcart_qs[0]
        if totalcart.movieitems.filter(movie__slug = movie.slug).exists():
            order_movie.quantity += 1
            order_movie.save()
            messages.info(request, "This item quantity was updated to your cart.")
        else:
            messages.info(request,"This item was added to your cart.")
            totalcart.movieitems.add(order_movie)
    else:
        # ordered_date = timezone.now()
        order = TotalCart.objects.create(checkout= False)
        TotalCart.cartname = User.objects.get.username
        messages.info(request, "This item was added to your cart.")
        order.movieitems.add(order_movie)
    # return redirect("home:movie", slug=slug)
    return redirect("home:cart")

def deletecart(request,slug):
    movie = get_object_or_404(Movie, slug=slug)
    totalcart = TotalCart.objects.filter(checkout=False)
    if OrderMovie.objects.filter(movie__slug = movie.slug).exists():
        OrderMovie.objects.filter(movie__slug = movie.slug).delete()
    return redirect('home:cart')


def removecart(request,slug):
    movie = get_object_or_404(Movie, slug=slug)
    totalcart = TotalCart.objects.filter(checkout=False)
    if OrderMovie.objects.filter(movie__slug = movie.slug).exists():
        quantity = OrderMovie.objects.get(movie__slug = movie.slug).quantity
        quantity -= 1
        OrderMovie.objects.filter(movie__slug = movie.slug).update( quantity = quantity)
    return redirect('home:cart')


def checkoutformView(request):
    form = CheckoutForm()
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            print('form.cleaned_data')
            messages.success(request, 'Thank you! Your items will be delivered soon.')
            Checkout.objects.create(**form.cleaned_data)
            form = CheckoutForm()
        else:
            print(form.errors)
    context = {
        "form": form
    }
    return render(request, 'checkout.html', context)







