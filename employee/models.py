from django.db import models
from django.urls import reverse

# Create your models here.
class employee(models.Model):
    profile = models.TextField()
    email_id    =models.CharField(max_length=120)
    eid         =models.CharField(max_length=10)
    name        =models.CharField(max_length=30)
    position   =models.TextField()
    languages       =models.CharField(max_length=30)
    skills      =models.CharField(max_length=30)
    profile_photo=models.ImageField(upload_to='profile_pics/')
    social_media = models.CharField(max_length=20)
    meetings = models.ManyToManyField("meeting",through= 'Meets')
    def __str__(self):
        return f'{self.name} : {self.position}'

class meeting(models.Model):
    title = models.CharField(max_length=20)
    date = models.DateField(blank=True,null=True)
    start_time = models.TimeField(blank=True,null=True)
    color = models.CharField(max_length=10,default='Black')
    end_time = models.TimeField(blank=True,null=True)
    summary = models.TextField(blank=True)
    participants = models.ManyToManyField(employee,through='Meets')
    email_id_of_participants = models.CharField(max_length=100,null=True,blank=True)
    link=models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return f'{self.id} : {self.title}'

class Meets(models.Model):
    m=models.ForeignKey("meeting",on_delete=models.CASCADE)
    e = models.ForeignKey("employee",on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.m} : {self.e}'
    