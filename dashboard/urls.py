from django.urls import path
from .views import *
from django.contrib.sitemaps.views import sitemap


app_name="dashboard"

urlpatterns = [
    path('', dashboard_view , name="dashboard"),   

    path('products/', product_list, name='product_list'),
    path('products/add/', product_add, name='product_add'),
    path('products/edit/<int:product_id>/', product_edit, name='product_edit'),
    path('products/delete/<int:product_id>/', product_delete, name='product_delete'),

    path('blogs/', blog_list, name='blog_list'),
    path('blogs/add/', blog_add, name='blog_add'),
    path('blogs/edit/<int:blog_id>/', blog_edit, name='blog_edit'),
    path('blogs/delete/<int:blog_id>/', blog_delete, name='blog_delete'),

    path('contacts/', contact_list, name='contact_list'),
    path('contacts/delete/<int:contact_id>/', contact_delete, name='contact_delete'),

    path('product-enquiries/', product_enquiry_list, name='product_enquiry_list'),
    path('product-enquiries/delete/<int:enquiry_id>/', product_enquiry_delete, name='product_enquiry_delete'),
    path('backup', backup_database, name='backup_database'), 
    path('login', login_view , name='login'),
    path('logout', logout_view, name='logout'),
    path('forgot_password', forgot_password_view , name='forgot_password'),
    path('reset/<str:uidb64>/<str:token>/', password_reset_confirm, name='password_reset_confirm'),
    path('authentication_error', custom_404_error, name='authentication_error'),
]
