
from django.conf.urls import url
from .views import *

urlpatterns = [
	#The (?P<fight_card_id>[0-9]+) grabs what is after the ? in the url and puts
	#it into the variable fight_card_id passed into the view function.
    url(r'fightcard', display_fight_card, name="display_fight_card"),
    url(r'upcoming_cards/', display_upcoming_cards, name="display_upcoming_cards"),
]
