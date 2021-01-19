from django.contrib import admin
from . import models

class ChoiceInline(admin.TabularInline):
    model = models.Choice
    extra = 1   #tedad namayesh Choice

@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_filter = ('text','pub_date') #create fillter for search
    inlines = [ChoiceInline] #rel inline

@admin.register(models.Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text','question') #display fields in lists
    fields = ['question',('text','vote')] #location fields in create page

@admin.register(models.Username)
class UsernameAdmin(admin.ModelAdmin):
    list_display = ('id','username')
