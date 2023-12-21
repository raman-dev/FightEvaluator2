from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('fighters/search/',views.fighter_search, name='fighter_search'),
    path('fighters/create-fighter',views.create_fighter, name='create_fighter'),

    path('matchup/create-matchup',views.create_matchup, name='create_matchup'),
    path('matchup/delete-matchup/<int:matchupId>',views.delete_matchup, name='delete_matchup'),

    path('test_post',views.test_post, name='test_post'),
]