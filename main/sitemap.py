from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from main.models import Product, Blog  # Import your models

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home', 'about', 'contact', 'terms_conditon', 'privacy_policy', 'cancellation_refund_policy', 'services']  # Add your static views here

    def location(self, item):
        return reverse(f'main:{item}')

class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Product.objects.all()

    def location(self, obj):
        return reverse('main:product-detail', args=[obj.slug])  # Adjust as per your URL structure

# class BlogSitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.6

#     def items(self):
#         return Blog.objects.all()

#     def lastmod(self, obj):
#         return obj.created_at  # or updated_at if you have it

#     def location(self, obj):
#         return reverse('main:blog_details', args=[obj.slug])  # Adjust as per your URL structure
    
sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
    # 'blogs': BlogSitemap,
}