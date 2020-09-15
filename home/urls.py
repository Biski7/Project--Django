from django.urls import path
from .views import HomeView, TvGenre, MovieGenre, SearchViewSeries, SearchViewMovies,signup, OrderView, MovieDetailView, SeriesDetailView, add_to_cart, checkoutformView,removecart, deletecart
app_name = "home"

urlpatterns =[
    path('',HomeView.as_view(), name='home'),
    path('movie/<slug>', MovieDetailView.as_view(), name='movie'),
    path('series/<slug>', SeriesDetailView.as_view(), name='series'),
    path('tGenre',TvGenre.as_view(), name='tvgenre'),
    path('mGenre',MovieGenre.as_view(), name='moviegenre'),
    path('searchmovies',SearchViewMovies.as_view(), name='searchmovies'),
    path('searchseries',SearchViewSeries.as_view(), name='searchseries'),
    path('signup',signup,name= 'signup'),
    path('cart',OrderView.as_view(),name='cart'),
    path('add-to-cart/<slug>',add_to_cart, name='add-to-cart'),
    path('checkout',checkoutformView, name='checkout'),
    path('removecart/<slug>', removecart, name='removecart'),
    path('deletecart/<slug>', deletecart, name='deletecart'),
]