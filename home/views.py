from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from home.models import Settings
from home.models import ContactForm,Contact_message
from django.contrib import messages
from products.models import Category,Products, Images,Comment
from home.forms import SearchForm
# Create your views here.

def home(request):
    setting=Settings.objects.get(pk=1)
    category=Category.objects.all()
    product_slider=Products.objects.all()
    product_latest=Products.objects.all().order_by('id')[:4]
    product_picked=Products.objects.all().order_by('?')[:4]
    page='home'
    context={
        'setting':setting,
        'page':page,
        'category':category,
        'product_slider':product_slider,
        'product_latest':product_latest,
        'product_picked':product_picked
        }
    return render(request,'index.html',context)

def aboutus(request):
    setting=Settings.objects.get(pk=1)
    category=Category.objects.all()
    context={
        'setting':setting,
        'category':category,
    }
    return  render(request,'about.html',context)
def contact(request):
    if request.method=="POST":
        form=ContactForm(request.POST)
        if form.is_valid():
            data=Contact_message()
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.email=form.cleaned_data['email']
            data.address=form.cleaned_data['email']
            data.city=form.cleaned_data['city']
            data.country=form.cleaned_data['country']
            data.telephone=form.cleaned_data['telephone']
            data.save()
            messages.success(request,'your message has been sent')
            return HttpResponseRedirect('/contact')

    setting=Settings.objects.get(pk=1)
    category=Category.objects.all()
    form=ContactForm
    context={
        'setting':setting,
        'form':form,
        'category':category,
    }
    return  render(request,'contact.html',context)

def category_products(request,id,slug):
    products=Products.objects.filter(category_id=id)
    category=Category.objects.all()
    context={
        'category':category,
        'products':products
        }
    return render(request,'category_products.html',context)

def search(request):
    if request.method=='POST':
        form=SearchForm(request.POST)
        if form.is_valid():
            query=form.cleaned_data['query']
            catid=form.cleaned_data['catid']
            if catid==0:
                products=Products.objects.filter(title__icontains=query)
            else:
                products=Products.objects.filter(title__icontains=query,category_id=catid)
            category=Category.objects.all()
            context={
                'products':products,
                'category':category,
                'query':query
            }
            return render(request,'search.html',context)
    return HttpResponseRedirect('/home')

def product_detail(request,id,slug):
    product=Products.objects.get(pk=id)
    category=Category.objects.all()
    image=Images.objects.filter(product_id=id)
    comments=Comment.objects.filter(product_id=id)
    context={
                'product':product,
                'category':category,
                'image':image,
                'comments':comments
            }
    return render(request,'product.html',context)