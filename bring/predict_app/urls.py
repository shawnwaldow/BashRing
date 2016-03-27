
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'(?P<fight_card_id>[0-9]+)', display_fight_card, name="display_fight_card")
]
