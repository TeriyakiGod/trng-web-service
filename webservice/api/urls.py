from django.urls import path
from . import views

urlpatterns = [
    path('rand/int', views.get_rand_int, name='rand_int'),
    path('rand/float', views.get_rand_float, name='rand_float'),
    path('rand/bytes', views.get_rand_bytes, name='rand_bytes'),
    path('rand/string', views.get_rand_string, name='rand_char'),
    path('rand/sequence', views.get_rand_sequence, name='rand_sequence'),
    path('rand/coin', views.get_rand_coin, name='rand_coin'),
    path('rand/dice', views.get_rand_dice, name='rand_dice'),
    path('rand/lotto', views.get_rand_lotto, name='rand_lotto')
]