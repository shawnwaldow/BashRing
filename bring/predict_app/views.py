
"""Do the View."""
#we added the last one for url var passing a '?'
from django.shortcuts import render, get_object_or_404

#We added this to handle the HttpResponse in this particular manner.
from django.http.response import HttpResponse

#Allow getting things from DB
from .models import Fight_Card, Fighter, Bout, User_Prediction, Method, Ring_User

from django.http import JsonResponse
import json
from django.shortcuts import render

from datetime import datetime, timedelta

# for sorted
import operator

#For making all datetimes aware. Must install in venv!
import pytz

# Create your views here.

def display_predict_bout(request, bout_id):
	"""Take a bout number from the url and allow a vote"""
	print("passed bout number", bout_id)
	bout = get_object_or_404(Bout, pk=bout_id)
	print(bout)
	context = {"bout":bout}
	return render(request, 'predict_app/predict_a_bout.html', context)

def display_fight_card(request, fight_card_id=0):
	"""experimenting with django templates. ONLY FOR MVP.
	MUST MUST MUST IMPLEMENT FILTERS INSTEAD"""
	print("passed fight card id", fight_card_id)

	fight_card_id = int(fight_card_id)
	fight_card = get_object_or_404(Fight_Card, pk=fight_card_id)
	
	all_bouts = Bout.objects.all()
	this_cards_bouts = []

	for tussle in all_bouts:

		if tussle.fight_card_id.id == fight_card_id:
			this_cards_bouts.append(tussle)

	this_cards_bouts.sort(key=operator.attrgetter('bout_importance_on_card'))
	print(this_cards_bouts)

	context = {
		'fight_card': fight_card, 
		'this_cards_bouts': this_cards_bouts
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

def submit_vote(request):
	"""Handles vote submissions via AJAX."""

	if request.method == 'POST':
		print(request.body)
		#decode request body from bytecode to normal
		data_json = request.body.decode('utf-8')
		print("suck-cess-pool", data_json)

		#turn the json string into a python object
		data = json.loads(data_json)

		#Work with the info in the json object to make sure it is in the right form to instantiate a new User_Prediction.
		#Is this the best place to do this?
		#Work back to adding round final and also sub to the template, js, and here.
		
		###Ack go back and redesign the model to do away with this.
		dict_const_to_pk={
			'SUB':3,
			'TKO':5, 
			'KO':2,
			'UNAN_DEC':7,
			'SPLIT_DEC':8,
			'DRAW':4,
			'NC':6,
			'INCOMPLETE':1
			}

		usersWinner = get_object_or_404(Fighter, pk=data['fighter_id'])
		usersMethod = get_object_or_404(Method, pk=dict_const_to_pk[data['method']])
		print("methd", usersMethod)
		usersBout = get_object_or_404(Bout, pk=data['bout_id'])
		print("OK BOUT",usersBout)
		aUser = get_object_or_404(Ring_User, pk=1) 
		print("OK user",aUser)


		aPrediction = User_Prediction(winner=usersWinner, method=usersMethod, round_final=3, confidence=data['confidence'], excitement=data['excitement'], attachment=data['attachment'], bout_id = usersBout, ring_user_id = aUser)
		aPrediction.save()
		print(aPrediction)

		# # Get the choice at that id
		# choice = Choice.objects.get(pk=int(data['choice_id']))

		# # Increment the votes of the choice by 1
		# choice.votes += 1

		# #save the updated objec choice to db
		# choice.save()

		# #Get all the choices for the question just voted on
		# question = Question.objects.get(pk=int(data['question_id']))

		# question_choices = question.choice_set.all()

		response = ["pickles", "mayo", "mysery meat"]

		# #loop through choices and dictionize
		# for choice in question_choices:
		# 	c_dict = {
		# 		'id': choice.id,
		# 		'text': choice.choice_text,
		# 		'votes': choice.votes
		# 	}


		# 	response.append(c_dict)
		

	return JsonResponse({'data': response})