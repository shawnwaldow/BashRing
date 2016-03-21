from django.contrib import admin
from .models import Ring_User, Fighter, Method, Fight_Card, Bout, User_Prediction, Weight_Class
# Register your models here.

admin.site.register(Ring_User)
admin.site.register(Fighter)
admin.site.register(Method)
admin.site.register(Fight_Card)
admin.site.register(Bout)
admin.site.register(User_Prediction)
admin.site.register(Weight_Class)