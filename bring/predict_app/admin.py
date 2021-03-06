from django.contrib import admin
from .models import Ring_User, Fighter, Method, Fight_Card, Bout, User_Prediction, Weight_Class
# Register your models here.

class BoutAdmin(admin.ModelAdmin):
	list_display = [
		'fight_card_id',
		'fighter1',
		'fighter2',
		'method_id',
		'weight_class',
		'max_rounds',
		'fighter1_odds',
		'fighter2_odds',
		'bout_importance_on_card',
		'id'
		]

	def id(self, obj):
		return obj.id

class Ring_User_Admin(admin.ModelAdmin):
	list_display = [
		'first_name',
		'last_name',
		'accuracy',
		'experience',
		'avatar',
		'id',
		'user_id'
		]
	def id(self, obj):
		return obj.id

# class Method_Admin(admin.ModelAdmin):
# 	list_display = [
# 		'INCOMPLETE',
# 		'SUB',
# 		'TKO',
# 		'KO',
# 		'UNAN_DEC',
# 		'SPLIT_DEC',
# 		'DRAW',
# 		'NC',
# 		'id'
# 	]
# 	def id(self, obj):
# 		return obj.id


admin.site.register(Ring_User,Ring_User_Admin)
admin.site.register(Fighter)
admin.site.register(Method)
admin.site.register(Fight_Card)
admin.site.register(Bout, BoutAdmin)
admin.site.register(User_Prediction)
admin.site.register(Weight_Class)