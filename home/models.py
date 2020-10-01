from django.db import models
from django.forms import ModelForm
from django.forms import TextInput

# Create your models here.
class Settings(models.Model):
    STATUS=(
        ('True','True'),
        ('False','False')
    )

    title=models.CharField(max_length=150)
    company=models.CharField(max_length=255)
    keywords=models.CharField(max_length=225)
    description=models.CharField(max_length=225)
    address=models.CharField(blank=True,max_length=255)
    phone=models.CharField(blank=True,max_length=15)
    fax=models.CharField(blank=True,max_length=15)
    email=models.EmailField(max_length=255)
    smtpserver=models.CharField(blank=True,max_length=15)
    smtpport=models.CharField(blank=True,max_length=15)
    smtppassword=models.CharField(blank=True,max_length=15)
    smtpemail=models.CharField(blank=True,max_length=15)
    facebook=models.CharField(blank=True,max_length=255)
    instagram=models.CharField(blank=True,max_length=255)
    twitter=models.CharField(blank=True,max_length=255)
    status=models.CharField(max_length=10,choices=STATUS)
    aboutus=models.TextField(blank=True,max_length=255)
    contactus=models.TextField(blank=True,max_length=255)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Contact_message(models.Model):
    STATUS=(
        ('New','New'),
        ('Read','Read'),
        ('Closed','Closed'),
    )
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=225)
    email=models.EmailField(blank=False,max_length=30)
    address=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    country=models.CharField(max_length=255)
    status=models.CharField(max_length=10,choices=STATUS)
    telephone=models.CharField(max_length=11)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.first_name+' '+self.last_name

class ContactForm(ModelForm):
    class Meta:
        model=Contact_message
        fields=['first_name','last_name','email','address','city','country','telephone']
        widget={
            'first_name':TextInput(attrs={'class':'input','placeholder':'first_name'}),
            'last_name':TextInput(attrs={'class':'input','placeholder':'last_name'}),
            'email':TextInput(attrs={'class':'input','placeholder':'email'}),
            'address':TextInput(attrs={'class':'input','placeholder':'address'}),
            'city':TextInput(attrs={'class':'input','placeholder':'city'}),
            'country':TextInput(attrs={'class':'input','placeholder':'country'}),
            
            'telephone':TextInput(attrs={'class':'input','placeholder':'telephone'}),
        }
