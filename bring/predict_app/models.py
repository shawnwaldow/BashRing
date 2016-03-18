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
class User_Prediction(models.Model)
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
	image = models.ImageField(default="static/menu_images/anon_fighter_small.jpg", upload_to="fighter_images")
	wins = models.PositiveIntegerField()
	losses = models.PositiveIntegerField()
	draws = models.PositiveIntegerField()
	ncs = models.PositiveIntegerField()
	tkos = models.PositiveIntegerField()
	kos = models.PositiveIntegerField()
	decs = models.PositiveIntegerField()
	days_layoff = models.PositiveIntegerField()
	fudge = models.FloatField(default=1)
	spice = models.FloatField(default=1)
	batwings = models.PositiveIntegerField()
	water = models.FloatField(default=1)
"""
class Method(model.Model)
	#CONST
	incomplete = 
	win = 
	loss = 
	draw = 
	nc = 
	tko = 
	ko = 
	unan_dec = 
	split_dec = 

class FightCard(model.Model)
"""