from django.db import models

# Create your models here.
from django.db import models

class data(models.Model):
    user = models.CharField(max_length=50)
    device_no = models.CharField(max_length=50)
    time = models.DateTimeField(unique=True)
    current = models.CharField(max_length=20)
    temperature = models.CharField(max_length=20)
    voltage = models.CharField(max_length=20)
    humidity = models.CharField(max_length=20)