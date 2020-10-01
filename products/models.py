
from django.db import models
from django.utils.safestring import mark_safe
from mptt.models import MPTTModel,TreeForeignKey
from mptt.admin import DraggableMPTTAdmin
from django.urls import reverse
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms import TextInput
from ckeditor_uploader.fields import  RichTextUploadingField
# Create your models here.
class Category(MPTTModel):
    STATUS=(
        ('True','True'),
        ('False','False')
    )
    title=models.CharField(max_length=30)
    keywords=models.CharField(max_length=225)
    description=models.CharField(max_length=225)
    image=models.ImageField(blank=True,upload_to='images/')
    status=models.CharField(max_length=10,choices=STATUS)
    slug=models.SlugField(null=False,unique=True)
    parent=TreeForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    class MPTTMeta:
        order_insertion_by = ['title']
    
    def get_absolute_url(self):
        return reverse('category_detail',kwargs={'slug':self.slug})

    def __str__(self):                           # __str__ method elaborated later in
        full_path = [self.title]                  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

class Products(models.Model):
    STATUS=(
        ('True','True'),
        ('False','False')
    )
    title=models.CharField(max_length=30)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    keywords=models.CharField(max_length=225)
    description=models.CharField(max_length=225)
    image=models.ImageField(blank=True,upload_to='images/')
    status=models.CharField(max_length=10,choices=STATUS)
    slug=models.SlugField(null=False,unique=True)
    parent=models.ForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    details=RichTextUploadingField()
    amount=models.IntegerField(default=0)
    price=models.FloatField()
    def __str__(self):
        return self.title
        
    def image_tag(self):
        return mark_safe('<img src={} height="50"/>'.format(self.image.url))
    
    
    image_tag_short_description='Image'

    def get_absolute_url(self):
        return reverse('category_detail',kwargs={'slug':self.slug})

class Images(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    title=models.CharField(max_length=50,blank=True)
    image=models.ImageField(blank=True,upload_to='images/')

    def __str__(self):
        return self.title
  



class Comment(models.Model):
    STATUS=(
        ('New','New'),
        ('True','True'),
        ('False','False')
    )
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subject=models.CharField(max_length=50,blank=True)
    comment=models.CharField(max_length=250,blank=True)
    status=models.CharField(max_length=10,choices=STATUS)
    rate=models.IntegerField(default=1)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model=Comment
        fields=['subject','comment']