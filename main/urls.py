from django.urls import path
from .views import *

app_name="main"

urlpatterns = [
    path('', index, name="home"),
    path('about', about, name="about"),
    path('terms-condition', terms_condition, name="terms_conditon"),
    path('privacy-policy', privacy_policy, name="privacy_policy"),
    path('cancellation-refund-policy', cancellation_policy, name="cancellation_refund_policy"),
    # path('blog', BlogListView.as_view(), name="blog"),
    # path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_details'),
    path('services/', ProductListView.as_view(), name='services'),
    path('services/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('contact', contact, name="contact"),
    path("robots.txt", RobotsTxtView.as_view(content_type="text/plain"), name="robots"),
]
