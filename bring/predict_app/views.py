 #we added the last one for url var passing a '?'
from django.shortcuts import render, get_object_or_404

#We added this to handle the HttpResponse in this particular manner.
from django.http.response import HttpResponse

#Allow getting things from DB
from .models import Fight_Card, Fighter, Bout

from django.http import JsonResponse

import json

from django.shortcuts import render
from datetime import datetime, timedelta

#For making all datetimes aware. Must install in venv!
import pytz

# Create your views here.

def display_fight_card(request, fight_card_id=1):
	"""experimenting with django templates. not for production"""
	print("passed fight card id", fight_card_id)

	fight_card = get_object_or_404(Fight_Card, pk=fight_card_id)
	fighter1 = get_object_or_404(Fighter, pk=1)
	fighter2 = get_object_or_404(Fighter, pk=2)
	array = [0,1,2,3,4]
	main_bout = get_object_or_404(Bout, pk=1)
	bout_string = preview_a_bout(main_bout)


	context = {
		'fight_card': fight_card, 
		'fighter1': fighter1, 
		'fighter2': fighter2, 
		'array': array, 
		'bout': get_object_or_404(Bout, pk=1), 
		'main_bout': main_bout
	}

	return render(request, 'predict_app/predict_a_card.html', context)

def display_upcoming_cards(request):
	"""display all cards for the next 30 days. This function badly need filters
	to improve scalibility. This is a prototype for demonstration purposes 
	only."""
	utc=pytz.UTC
	#Make local to user
	now = datetime.now()
	servertime = now
	
	servertime = utc.localize(servertime)

	#Make 'upcoming' a list of cards in the next 30 days starting with the most
	#immeadiate
	fight_cards = Fight_Card.objects.all()
	upcoming=[]
	for card in fight_cards:
		if (card.start_time > servertime) and (card.start_time < servertime + timedelta(days=32)):
			upcoming.append(card)
	
	upcoming.sort(key=lambda r: r.start_time)
	print(upcoming)
	#Make a dict of keys with card number and values as headliner bouts
	headliners = {}
	
	for event in upcoming:
		headliners[event.id] = 0

	print(headliners)

	all_bouts = Bout.objects.all()


	# making a dict headliners={fight_card_id: headline_bout_obj}
	for each in headliners.keys():
		print(each)
		for tussle in all_bouts:
			# look at the fight card id of every bout in the db for ones that are
			# in our headliners dictonary. For these then check to see if their
			# importance_on_card == 0. The zeroth bouts are the headliners.
			if (tussle.fight_card_id.id == each) and (tussle.bout_importance_on_card == 0):
				headliners[each] = tussle

	#Because i could not get the dictionary keys to resolve when passed
	#values from an array in the template, we must build up this simple
	#matrix to hand off instead:
	#next_30_days[x]=tuple(fight_card_obj, bout_obj)

	next_30_days=[]
	for event in upcoming:
		tup = (event, headliners[event.id])
		next_30_days.append(tup)


	print("event id: headline bout id", headliners)

	context = {
		'now': now, 'next_30_days': next_30_days, 'upcoming': upcoming
	}

	return render(request, 'predict_app/display_upcoming_cards.html', context)

def preview_a_bout(a_bout):
	"""Displays an overview of a bout."""
	#fighter1 = get_object_or_404(Fighter, pk=1)
	#fighter2 = get_object_or_404(Fighter, pk=2)

	bout_span=a_bout.fighter1.last_name+" vs. "+a_bout.fighter2.last_name
	return bout_span