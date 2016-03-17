from django.db import models

# Create your models here.

class Ring_User(models.Model):

	first = models.TextField(max_length=64, default='noname')
	last = models.TextField(max_length=64, default='noname')
	accuracy = models.FloatField(default=1)
	experience = models.PositiveIntegerField(default=0)
	avatar = models.ImageField

class User_Prediction(models.Model)
	bout_id = models.ForeignKey(Bout)
	winner = models.ForeignKey(Fighter)
	method = models.ForeignKey(Method)
	round_final = models.PositiveSmallIntegerField()
	confidence = models.ForeignKey(Likert)
	excitement = models.ForeignKey(Likert)
	attachment = models.ForeignKey(Likert)
	ring_user_id = models.ForeignKey(Ring_User)



#relational table

use related name on fighter1 and 2 relationship
