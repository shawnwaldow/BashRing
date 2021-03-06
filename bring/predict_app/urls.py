from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from .views import *

urlpatterns = [
	#The (?P<fight_card_id>[0-9]+) grabs what is after the ? in the url and puts
	#it into the variable fight_card_id passed into the view function.
    url(r'fightcard/(?P<fight_card_id>[0-9]+)', display_fight_card, name="display_fight_card"),
    url(r'upcoming_cards/', display_upcoming_cards, name="display_upcoming_cards"),
    url(r'predict_bout/(?P<bout_id>[0-9]+)', display_predict_bout, name="display_predict_bout"),
    url(r'submit_vote$', submit_vote),
    url(r'accounts/profile/', display_users_ring),
    url(r'fix/(?P<bout_id>[0-9]+)', declare_winners_by_fight_card),
    url(r'recent_past_cards/', display_recent_past_cards, name="recent_past_cards"),
    url(r'^', display_home)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

