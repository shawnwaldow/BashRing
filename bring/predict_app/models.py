#python manage.py flush deletes the entire database
from django.db import models

#import stuff for AUTH_USER_MODEL
from django.conf import settings

# Create your models here.

class Ring_User(models.Model):

	first_name = models.CharField(max_length=64, default='noname')
	last_name = models.CharField(max_length=64, default='noname')
	accuracy = models.FloatField(default=1)
	experience = models.PositiveIntegerField(default=0)
	avatar = models.ImageField(default="static/menu_images/user1.png",upload_to="avatar_images")
"""

class User_Prediction(models.Model):
	#Foreign Keys
	bout_id = models.ForeignKey(Bout)
	winner = models.ForeignKey(Fighter)
	method = models.ForeignKey(Method)
	ring_user_id = models.ForeignKey(Ring_User)
	round_final = models.PositiveSmallIntegerField()
	#Remake these as a const Likert 
	confidence = models.PositiveIntegerField()
	excitement = models.PositiveIntegerField()
	attachment = models.PositiveIntegerField()
	note = models.TextField(max_length=255)
"""
class Fighter(models.Model):
	last_name = models.CharField(max_length=64, default=' ')
	first_name = models.CharField(max_length=64, default=' ')
	nick_name =  models.CharField(max_length=64, default=' ')
	statid = models.PositiveIntegerField(default=0)
	fighter_status = models.BooleanField()
	image = models.ImageField(default="static/menu_images/anon_fighter_small.jpg", upload_to="fighter_images")
	wins = models.PositiveIntegerField()
	losses = models.PositiveIntegerField()
	draws = models.PositiveIntegerField()
	ncs = models.PositiveIntegerField()
	tkos = models.PositiveIntegerField()
	kos = models.PositiveIntegerField()
	decs = models.PositiveIntegerField()
	subs = models.PositiveIntegerField(default=0)
	days_layoff = models.PositiveIntegerField()
	fudge = models.FloatField(default=1)
	spice = models.FloatField(default=1)
	batwings = models.PositiveIntegerField()
	water = models.FloatField(default=1)

class Method(models.Model):
	#CONST
	INCOMPLETE = 0
	SUB = 1
	TKO = 2 
	KO = 3
	UNAN_DEC = 4
	SPLIT_DEC = 5
	DRAW = 6
	NC =  7

	Result = (
		(INCOMPLETE, 'Incomplete'),
		(SUB, 'Submission'),
		(TKO, 'TKO'),
		(KO, 'KO'),
		(UNAN_DEC, 'Unanimous Decision'),
		(SPLIT_DEC, 'Split Decision'),
		(DRAW, 'Draw'),
		(NC, 'No Contest')
	)

	result = models.IntegerField(choices=Result, default=INCOMPLETE)

	def __str__(self):
		return self.Result[self.result][1]

class Fight_Card(models.Model):
	title = models.CharField(max_length=127)
	organization = models.CharField(max_length=64, default='UFC')
	start_time = models.DateField()
	complete = models.DateField()
