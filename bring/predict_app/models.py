#python manage.py flush deletes the entire database
from django.db import models

#import stuff for AUTH_USER_MODEL
from django.conf import settings

from datetime import datetime
# Create your models here.

class Ring_User(models.Model):

	first_name = models.CharField(max_length=64, default='noname')
	last_name = models.CharField(max_length=64, default='noname')
	accuracy = models.FloatField(default=1)
	experience = models.PositiveIntegerField(default=0)
	avatar = models.ImageField(default="static/menu_images/user1.png",upload_to="avatar_images")

	def __str__(self):
		return self.first_name+" "+self.last_name


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
	gender = models.BooleanField(default=True) #F=Female, T=Male


	def __str__(self):
		return self.first_name+" '"+self.nick_name+"' "+self.last_name



class Weight_Class(models.Model):
	#CONST
	#Women's Division
	ATOM_W = 9
	STRAW_W = 10
	FLY_W = 11
	BANTAM_W = 12
	FEATHER_W = 13

	#Men's Division
	FLY_M = 1
	BANTAM_M = 2
	FEATHER_M = 3
	LIGHT_M = 4
	WELTER_M = 5
	MIDDLE_M = 6
	LIGHT_HEAVY_M = 7
	HEAVY_M = 8

	Division = (

		(ATOM_W, "Women's Atomweight"),
		(STRAW_W, "Women's Strawweight"),
		(FLY_W, "Women's Flyweight"),
		(BANTAM_W, "Women's Bantamweight"),
		(FEATHER_W, "Women's Featherweight"),

		(FLY_M, "Men's Flyweight"),
		(BANTAM_M, "Men's Bantamweight"),
		(FEATHER_M, "Men's Featherweight"),
		(LIGHT_M, "Men's Lightweight"),
		(WELTER_M, "Men's Welterweight"),
		(MIDDLE_M, "Men's Middleweight"),
		(LIGHT_HEAVY_M, "Men's Light-Heavyweight"),
		(HEAVY_M, "Men's Heavyweight"),
	)

	division = models.IntegerField(choices=Division)

	def __str__(self):
		return self.Division[self.division][1]



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
	#GMT
	start_time = models.DateTimeField()
	end_time = 	models.DateTimeField(blank=True, default=datetime.now())
	organizations_id = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.organization + " " + self.title



class Bout(models.Model):
	fight_card_id = models.ForeignKey(Fight_Card)
	fighter1 = models.ForeignKey(Fighter, related_name="fighter_1")
	fighter2 = models.ForeignKey(Fighter, related_name="fighter_2")
	method_id = models.ForeignKey(Method)
	weight_class = models.ForeignKey(Weight_Class)
	max_rounds = models.PositiveIntegerField()
	fighter1_odds = models.IntegerField(default=100)
	fighter2_odds = models.IntegerField(default=-100)
	bout_importance_on_card = models.PositiveIntegerField(default=0)

	def __str__(self):
		return str(self.fight_card_id) +"'s bout: "+ str(self.fighter1) + " vs. "+ str(self.fighter2)



class User_Prediction(models.Model):
	#bout_id = models.ForeignKey(Bout)
	winner = models.ForeignKey(Fighter)
	method = models.ForeignKey(Method)
	round_final = models.PositiveIntegerField()
	confidence = models.PositiveIntegerField()
	excitement = models.PositiveIntegerField()
	attachment = models.PositiveIntegerField()
	note = models.TextField()
	ring_user_id = models.ForeignKey(Ring_User)
	bout_id = models.ForeignKey(Bout, default=0)
	#can we make a string here to show user name and each fighter name?!

	def __str__(self):
		return str(self.bout_id) + " Prediction by " + str(self.ring_user_id)



class BoutWinner(models.Model):
	bout_id = models.ForeignKey(Bout)
	fighter_id = models.ForeignKey(Fighter)


	def __str__(self):
		return "bout"+bout_id+":Winner"+fighter_id
