from django.contrib import admin
from .models import Movie, Tv, OrderMovie, TotalCart, Checkout, MajorItems, Trailers

# Register your models here.
admin.site.register(Movie)
admin.site.register(Tv)
admin.site.register(OrderMovie)
admin.site.register(TotalCart)
admin.site.register(Checkout)
admin.site.register(MajorItems)
admin.site.register(Trailers)