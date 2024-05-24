from django.contrib import admin
from .models import Pet
# Register your models here.


class PetAdmin(admin.ModelAdmin):
 list_display=('id','name','price','gender','animal_type','breed','age','description')



admin.site.register(Pet,PetAdmin)
