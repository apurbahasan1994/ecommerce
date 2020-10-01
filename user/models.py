from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import TextInput, EmailInput, Select, FileInput

# Create your models here.
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=11,blank=True)
    address=models.CharField(max_length=250,blank=True)
    city=models.CharField(max_length=250,blank=True)
    country=models.CharField(max_length=250,blank=True)
    image=models.ImageField(blank=True,upload_to='images/user')

    def __str__(self):
        return self.user.username
    
    def user_name(self):
        return self.user.first_name+' '+self.user.last_name+' ['+self.user.username+'] '

    def image_tag(self):
        return mark_safe('<img src="{}" height="50">'.format(self.image.url))

    
    image_tag_short_description='Image'


class SignUpForm(UserCreationForm):
    username=forms.CharField(max_length=250,label='User Name')
    first_name=forms.CharField(max_length=250,label='First Name')
    last_name=forms.CharField(max_length=250,label='last Name')
    email=forms.EmailField(max_length=250,label='Email')
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=50)

    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2']

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ( 'username','email','first_name','last_name')
        widgets = {
            'username'  : TextInput(attrs={'class': 'input','placeholder':'username'}),
            'email'     : EmailInput(attrs={'class': 'input','placeholder':'email'}),
            'first_name': TextInput(attrs={'class': 'input','placeholder':'first_name'}),
            'last_name' : TextInput(attrs={'class': 'input','placeholder':'last_name' }),
        }

CITY = [
    ('Dhaka', 'Dhaka'),
    ('Chitagong', 'Chitagong'),
    ('Rajshahi', 'Rajshahi'),
    ('Khulna', 'Khulna'),
    ('Sylhet', 'Sylhet'),
    ('Rangpur','Rangpur')
]
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city','country','image')
        widgets = {
            'phone'     : TextInput(attrs={'class': 'input','placeholder':'phone'}),
            'address'   : TextInput(attrs={'class': 'input','placeholder':'address'}),
            'city'      : Select(attrs={'class': 'input','placeholder':'city'},choices=CITY),
            'country'   : TextInput(attrs={'class': 'input','placeholder':'country' }),
            'image'     : FileInput(attrs={'class': 'input', 'placeholder': 'image', }),
        }