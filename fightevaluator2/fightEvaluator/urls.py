from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fighters/search/',views.fighter_search, name='fighter_search'),
]