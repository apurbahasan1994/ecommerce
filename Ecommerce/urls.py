from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
    path('',include('products.urls')),
     path('order/',include('order.urls')),
    path('user/',include('user.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]