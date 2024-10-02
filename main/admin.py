from django.contrib import admin
from main.models import Contact, Product, ProductEnquiry, Blog, MetaTag

# Register your models here.
admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(ProductEnquiry)
admin.site.register(Blog)

@admin.register(MetaTag)
class MetaTagAdmin(admin.ModelAdmin):
    list_display = ('page', 'title', 'description', 'keywords')
    search_fields = ('page', 'title')