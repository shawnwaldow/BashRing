
"""BashRing Fantasy MMA. The meat of the Django implementation of beta version 
1 MVP!!!"""



# We added this last one for url var passing a '?'
from django.shortcuts import render, get_object_or_404

# We added this to handle the HttpResponse in this particular manner.
from django.http.response import HttpResponse

# Allow getting things from DB
from .models import Fight_Card, Fighter, Bout, User_Prediction, Method, Ring_User, User

from django.http import JsonResponse
import json
from django.shortcuts import render

# For function sorted
import operator

# For making all datetimes aware. Must install in venv!
import pytz
from datetime import datetime, timedelta

# For django users and registration peewee
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def display_users_ring(request):
	"""This is the first page a ring_user sees after login."""
	# Do a query to find the Ring_User corresponding to the logged-in Django
	# user. If they are new the Ring_User.first_name will = "noname". Update
	# it to correspond to the django user username. This is for MVP only.
	print(Ring_User.objects.get(user_id=request.user))
	aUser = Ring_User.objects.get(user_id=request.user)	
	if aUser.first_name == "noname":
		aUser.first_name=request.user.get_username()

	return render(request, "predict_app/users_ring.html")


def display_home(request):
	"""This is the splash page users see at root directing them to login or 
	register"""

	return render(request, "predict_app/home.html")

def display_register(request):
	"""Display baked in Django registration form PEWEE"""

	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():

			print("updating valid")
			
			new_user = form.save()

			#Point them to display_users_ring() via predict_app/urls.py
			return HttpResponseRedirect("/accounts/profile/")
	else:

		form = UserCreationForm()

	return render(request, "registration/register.html", {

	'form': form,

	})


@login_required
def display_predict_bout(request, bout_id):
	"""Take a bout number from the url and allow ring_user to vote"""

	print("passed bout number", bout_id)

	bout = get_object_or_404(Bout, pk=bout_id)

	print(bout)

	context = {"bout":bout}

	return render(request, 'predict_app/predict_a_bout.html', context)

@login_required
def display_fight_card(request, fight_card_id=0):
	"""Display all the bouts on a given fight card. ONLY FOR MVP.
	MUST MUST MUST IMPLEMENT QUERYSETS INSTEAD"""
	print("passed fight card id", fight_card_id)

	#Things we grab from the url always come in as strings.
	fight_card_id = int(fight_card_id)
	fight_card = get_object_or_404(Fight_Card, pk=fight_card_id)
	
	#Sledgehammer! Call up all the cards ever in the bout. Fix after MVP.
	all_bouts = Bout.objects.all()
	this_cards_bouts = []

	for tussle in all_bouts:

		#
		if tussle.fight_card_id.id == fight_card_id:
			this_cards_bouts.append(tussle)

	this_cards_bouts.sort(key=operator.attrgetter('bout_importance_on_card'))
	print(this_cards_bouts)

	for bout in this_cards_bouts:
		#reverse lookup usuing queryset object
		print(bout.user_prediction_set.all())


	context = {
		'fight_card': fight_card, 
		'this_cards_bouts': this_cards_bouts
	}

	return render(request, 'predict_app/predict_a_card.html', context)


@login_required
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
	#Django object chaching might be a way to streamline this
	#use querysets when refactoring, f object might help, also maybe q objects
	fight_cards = Fight_Card.objects.all()
	upcoming=[]
	for card in fight_cards:
		if (card.start_time > servertime) and (card.start_time < servertime + timedelta(days=32)):
			upcoming.append(card)
	
	upcoming.sort(key=lambda r: r.start_time)
	#print(upcoming)
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

@login_required
def submit_vote(request):
	"""Handles vote submissions via AJAX."""
	#here is how you lookup a ring_user given current user
	print("HERRRRRRRRRRRRRRR", Ring_User.objects.get(user_id=request.user))
	if request.method == 'POST':
		
		#decode request body from bytecode to normal
		data_json = request.body.decode('utf-8')
		

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
		
		usersBout = get_object_or_404(Bout, pk=data['bout_id'])
		

		# Do a query to find the Ring_User corresponding to the logged-in Django
		# user.
		aUser = Ring_User.objects.get(user_id=request.user)
		


		aPrediction = User_Prediction(winner=usersWinner, method=usersMethod, round_final=3, confidence=data['confidence'], excitement=data['excitement'], attachment=data['attachment'], bout_id = usersBout, ring_user_id = aUser)
		aPrediction.save()
		

		response = usersBout.fight_card_id.id

		
		

	return JsonResponse({'data': response})