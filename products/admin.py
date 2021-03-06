from django.contrib import admin
from products.models import Category
from products.models import Products,Images,Comment
from mptt.admin import DraggableMPTTAdmin
class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields={'slug':('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Products,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Products,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

class ProductImageInline(admin.TabularInline):
    model=Images
    extra=1

class Productadmin(admin.ModelAdmin):
    list_display=['title','category','status','image_tag']
    readonly_fields=('image_tag',)
    list_filter=['category']
    inlines=[ProductImageInline]
    prepopulated_fields={'slug':('title',)}

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image','title']

    


# Register your models here.
admin.site.register(Category,CategoryAdmin2)
admin.site.register(Products,Productadmin)
admin.site.register(Images,ImagesAdmin)
