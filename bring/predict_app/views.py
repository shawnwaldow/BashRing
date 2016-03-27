from django.shortcuts import render, get_object_or_404 #we added the last one for url var passing?

#We added this to handle the HttpResponse in this particular manner.
from django.http.response import HttpResponse

#Allow getting things from DB
from .models import Fight_Card, Fighter, Bout

from django.http import JsonResponse

import json

from django.shortcuts import render
from datetime import datetime

#For making all datetimes aware. Must install in venv!
import pytz

# Create your views here.

def display_fight_card(request, fight_card_id=1):
	"""from question details"""
	print("passed fight card id", fight_card_id)

	fight_card = get_object_or_404(Fight_Card, pk=fight_card_id)
	fighter1 = get_object_or_404(Fighter, pk=1)
	fighter2 = get_object_or_404(Fighter, pk=2)
	array = [0,1,2,3,4]
	main_bout = get_object_or_404(Bout, pk=1)
	bout_string = preview_a_bout(main_bout)


	context = {
		'fight_card': fight_card, 'fighter1': fighter1, 'fighter2': fighter2, 'array': array, 'bout': get_object_or_404(Bout, pk=1), 'main_bout': main_bout
	}

	return render(request, 'predict_app/predict_a_card.html', context)

def display_upcoming_cards(request):
	"""display all cards for the next 30 days"""
	utc=pytz.UTC
	#Make local to user
	now = datetime.now()
	servertime = now
	
	servertime = utc.localize(servertime)

	#Make a list of cards in the next 30 days starting with the most immeadiate
	fight_cards = Fight_Card.objects.all()

	upcoming=[]
	for card in fight_cards:
		if card.start_time > servertime:
			upcoming.append(card)
	print(upcoming)
	#Make a dict of keys with card number and values as headliner bouts



	context = {
		'now': now
	}

	return render(request, 'predict_app/display_upcoming_cards.html', context)

def preview_a_bout(a_bout):
	"""Displays an overview of a bout."""
	#fighter1 = get_object_or_404(Fighter, pk=1)
	#fighter2 = get_object_or_404(Fighter, pk=2)

	bout_span=a_bout.fighter1.last_name+" vs. "+a_bout.fighter2.last_name
	return bout_span