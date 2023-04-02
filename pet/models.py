from django.db import models
from django.utils import timezone
from datetime import datetime
# Create your models here.
from django.contrib.auth.models import User

class Pet(models.Model):
    name = models.CharField(max_length=255)
    birth = models.DateField(null=True, default=timezone.now)
    sexe = models.BooleanField(null=True)
    img = models.CharField(max_length=255)
    
    @property
    def height(self):
        return PetHeight.objects.filter(pet=self).order_by('date').first().height


class PetHeight(models.Model):
    height = models.FloatField()
    date = models.DateField(null=True, default=timezone.now)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)


class PetNeeds(models.Model):
    date_in = models.DateTimeField(default=timezone.now)
    date_out = models.DateTimeField(null=True)
    who = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=255, null=True)
    poop = models.BooleanField(default=False, null=True)
    pee = models.BooleanField(default=False, null=True)
    walk = models.BooleanField(default=False, null=True)
    done = models.BooleanField(default=False)

    @property
    def delta(self):
        time = self.date_out - self.date_in
        # time_hour = '{:02d}'.format(int(time.seconds / 60 / 24))
        time_minute = '{:02d}'.format(int((time.seconds / 60) % 60 ))
        return time_minute + ' minutes'
    
class PetFeeds(models.Model):
    date = models.DateTimeField(default=timezone.now)
    who = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity_given = models.IntegerField()
    quantity_left = models.IntegerField()

    @property
    def eated(self):
        return self.quantity_given - self.quantity_left
