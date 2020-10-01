from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from products.models import Category
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from user.models import UserProfile,SignUpForm
from django.contrib.auth.decorators import login_required
from user.models import UserUpdateForm,UserChangeForm,ProfileUpdateForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from order.models import Order,OrderProduct
from products.models import Comment

# Create your views here.
@login_required(login_url='/login')  # Check login
def index(request):
    category=Category.objects.all()
    current_user=request.user
    profile=UserProfile.objects.get(user_id=current_user.id)
    context={
                'category':category,
                'profile':profile
            }
    return render(request,'profile.html',context)


def log_in(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user=request.user
            user_profile=UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage']=user_profile.image.url
            return HttpResponseRedirect('/home')
        else:
            messages.success(request,'Your username or password is incorrect!')
            return HttpResponseRedirect('/user/login')
    category=Category.objects.all()
    context={
                'category':category,
            }
    return render(request,'login_form.html',context)

def logoutfunc(request):
    logout(request)
    return HttpResponseRedirect('/home')

def signup(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            user=authenticate(username=username,password=password)
            login(request,user)
            current_user = request.user
            data=UserProfile()
            data.user_id=current_user.id
            data.image="images/users/index.png"
            data.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/home')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect('/user/signup')
    else:
        form=SignUpForm()
        category=Category.objects.all()
        context={
                'category':category,
                'form':form,
               }

        return render(request,'signup.html',context)

@login_required(login_url='/login') # Check login
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user/profile')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile) #"userprofile" model -> OneToOneField relatinon with user
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)

@login_required(login_url='/login') # Check login
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>'+ str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'user_password.html', {'form': form,'category': category})
    

def user_order(request):
    category = Category.objects.all()
    current_user=request.user
    orders=Order.objects.filter(user_id=current_user.id)
    context = {
            'category': category,
            'orders':orders
        }
    return render(request,'user_orders.html',context)

@login_required(login_url='/login') # Check login
def user_order_detail(request,id):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)

@login_required(login_url='/login') # Check login
def orders_product(request):
    category = Category.objects.all()
    current_user = request.user
    orderitems=OrderProduct.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_products.html', context)
    return HttpResponse('order')

def user_comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'comments': comments,
    }
    return render(request, 'user_comments.html', context)

@login_required(login_url='/login') # Check login
def user_delete_comment(request,id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted..')
    return HttpResponseRedirect('/user/user_delete_comment')