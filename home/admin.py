from django.contrib import admin
from home.models import Settings,Contact_message

admin.site.register(Settings)
class ContactmessageAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','update_at','status']
    readonly_fields=['first_name','last_name','telephone','city','country','email']
admin.site.register(Contact_message,ContactmessageAdmin)




# Register your models here.

