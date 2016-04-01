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
	organizations_id=models.PositiveIntegerField(default=0)
	sherdog_id=models.PositiveIntegerField(default=0)
	fighter_status = models.BooleanField(blank=True,)
	image_url = models.CharField(max_length=254, default="static/menu_images/anon_fighter_small.jpg")
	wins = models.PositiveIntegerField()
	losses = models.PositiveIntegerField()
	draws = models.PositiveIntegerField()
	ncs = models.PositiveIntegerField(blank=True,)
	tkos = models.PositiveIntegerField(blank=True,)
	kos = models.PositiveIntegerField(blank=True,)
	decs = models.PositiveIntegerField(blank=True,)
	subs = models.PositiveIntegerField(blank=True,default=0)
	days_layoff = models.PositiveIntegerField(blank=True,)
	fudge = models.FloatField(blank=True,default=1)
	spice = models.FloatField(blank=True,default=1)
	batwings = models.PositiveIntegerField(blank=True,)
	water = models.FloatField(blank=True,default=1)
	gender = models.BooleanField(default=True) #F=Female, T=Male

	def __str__(self):
		return self.first_name+" "+self.last_name



class Weight_Class(models.Model):
	#CONST
	#Women's Division
	ATOM_W = 0
	STRAW_W = 1
	FLY_W = 2
	BANTAM_W = 3
	FEATHER_W = 4

	#Men's Division
	FLY_M = 5
	BANTAM_M = 6
	FEATHER_M = 7
	LIGHT_M = 8
	WELTER_M = 9
	MIDDLE_M = 10
	LIGHT_HEAVY_M = 11
	HEAVY_M = 12

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
	title = models.CharField(max_length=127, default=' ')
	short_description = models.CharField(max_length=500, default=' ')
	organization = models.CharField(max_length=63, default='UFC')
	organizations_id = models.PositiveIntegerField(default=0)
	#GMT
	start_time = models.DateTimeField()
	end_time = 	models.DateTimeField(blank=True, default=datetime.now())
	


	def __str__(self):
		return self.organization + " " + self.title



class Bout(models.Model):
	fight_card_id = models.ForeignKey(Fight_Card)
	fighter1 = models.ForeignKey(Fighter, related_name="fighter_1")
	fighter2 = models.ForeignKey(Fighter, related_name="fighter_2")
	method_id = models.ForeignKey(Method)
	weight_class = models.ForeignKey(Weight_Class)
	max_rounds = models.PositiveIntegerField(blank=True, default=3)
	fighter1_odds = models.IntegerField(blank=True,default=100)
	fighter2_odds = models.IntegerField(blank=True,default=-100)
	bout_importance_on_card = models.PositiveIntegerField(default=1)


	def __str__(self):
		return str(self.fight_card_id) +"'s bout: "+ str(self.fighter1) + " vs. "+ str(self.fighter2)



class User_Prediction(models.Model):
	winner = models.ForeignKey(Fighter)
	method = models.ForeignKey(Method)
	round_final = models.PositiveIntegerField()
	confidence = models.PositiveIntegerField()
	excitement = models.PositiveIntegerField()
	attachment = models.PositiveIntegerField()
	ring_user_id = models.ForeignKey(Ring_User)
	bout_id = models.ForeignKey(Bout, default=0)	
	#can we make a string here to show user name and each fighter name?!

	def __str__(self):
		return str(self.bout_id) + " Prediction by " + str(self.ring_user_id)



class BoutWinner(models.Model):
	bout_id = models.ForeignKey(Bout)
	fighter_id = models.ForeignKey(Fighter)


	def __str__(self):
		return "bout"+str(self.bout_id)+":Winner"+str(self.fighter_id)
