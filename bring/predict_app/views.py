from django.shortcuts import render, get_object_or_404 #we added the last one for url var passing?

#We added this to handle the HttpResponse in this particular manner.
from django.http.response import HttpResponse

#Allow getting things from DB
from .models import Fight_Card, Fighter, Bout

from django.http import JsonResponse

import json

from django.shortcuts import render

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

def preview_a_bout(a_bout):
	"""Displays an overview of a bout."""
	#fighter1 = get_object_or_404(Fighter, pk=1)
	#fighter2 = get_object_or_404(Fighter, pk=2)

	bout_span=a_bout.fighter1.last_name+" vs. "+a_bout.fighter2.last_name
	return bout_span