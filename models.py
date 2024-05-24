from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Pet(models.Model):
    gender_choices = (("male", "Male"), ("female", "Female"))
    animal_type_choices = (("D", "Dog"), ("C", "Cat"))
    
    pimage = models.ImageField(upload_to="media", null=True, blank=True)
    name = models.CharField(max_length=30, verbose_name="Pet Name")
    price = models.FloatField(default=10, verbose_name="Price")
    animal_type = models.CharField(max_length=30, choices=animal_type_choices)
    breed = models.CharField(max_length=30, verbose_name="Pet Breed")
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=gender_choices)
    description = models.CharField(max_length=400)
    is_active = models.BooleanField(default=True)

    

    def __str__(self):
        return self.name

class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Pet,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)

class Order(models.Model):
    order_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(Pet,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)