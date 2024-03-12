from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('predictions',views.predictions,name="predictions"),

    # path('focusTest',views.focusTest, name='focusTest'),
    path('events/results/<int:eventId>',views.getFightEventResults, name='results'),

    path('<int:eventId>',views.indexById,name='indexById'),
    path('events/',views.events),
    path('events/<int:eventId>/predictions',views.event_predictions, name='event_predictions'),#not working

    path('fighters/search/',views.fighter_search, name='fighter_search'),#working
    path('fighters/create-fighter',views.create_fighter, name='create_fighter'),#working
    path('fighters/update-fighter/<int:fighterId>',views.update_fighter, name='update_fighter'),#working

    path('assessment/<int:fighterId>',views.assessment_index, name='assessment'),#working
    path('assessment/update',views.update_assessment, name='update_assessment'),#working

    path('notes/create-note',views.create_note, name='create_note'),#working
    path('notes/delete-note/<int:noteId>',views.delete_note, name='delete_note'),#working

    path('matchup/create-matchup',views.create_matchup, name='create_matchup'),#working
    path('matchup/update-matchup/<int:matchupId>',views.update_matchup, name='update_matchup'),#working
    path('matchup/delete-matchup/<int:matchupId>',views.delete_matchup, name='delete_matchup'),#working
    path('matchup/<int:matchupId>',views.matchup_index, name='matchup'),#working

    path('matchup/update-event-likelihood/',views.updateMatchUpEventLikelihood, name='update_event_likelihood'),#working
    path('matchup/update-event-prediction/',views.updateMatchUpEventPrediction,name='update_event_prediction'),#not working
]