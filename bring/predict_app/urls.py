
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'(?P<fight_card_id>[0-9]+)', display_fight_card, name="display_fight_card"),
    url(r'upcoming_cards/', display_upcoming_cards, name="display_upcoming_cards")
]
