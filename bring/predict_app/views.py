from django.shortcuts import render, get_object_or_404 #we added the last one for url var passing?

#We added this to handle the HttpResponse in this particular manner.
from django.http.response import HttpResponse

#Allow getting things from DB
from .models import Fight_Card, Fighter

from django.http import JsonResponse

import json


from django.shortcuts import render

# Create your views here.

def display_fight_card(request, fight_card_id):
"""from question details"""
	print("passed fight card id", fight_card_id)

	fight_card = get_object_or_404(Fight_Card, pk=fight_card_id)

	fight_card = {
		'fight_card': fight_card,
	}

	return render(request, 'predict_app/predict_a_card.html', context)
