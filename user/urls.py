from django.urls import path,include
from user import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('profile/',views.index,name='profile'),
    path('login',views.log_in,name="login"),
    path('logout/',views.logoutfunc,name='logoutfunc'),
    path('signup/',views.signup,name='signup'),
    path('userupdate/',views.user_update,name='user_update'),
    path('userpassword/',views.user_password,name='user_password'),
    path('user_order/',views.user_order,name='user_order'),
    path('user_order_detail/<int:id>',views.user_order_detail,name='user_order_detail'),
    path('orders_product/',views.orders_product,name='orders_product'),
    path('user_comments/',views.user_comments,name='user_comments'),
    path('user_delete_comment/<int:id>',views.user_delete_comment,name='user_delete_comment')
]
