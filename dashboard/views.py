import subprocess
import os
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import  login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from main.models import Blog, Contact, Product, ProductEnquiry
# import requests

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
     
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
                return redirect('dashboard:dashboard')
        else:
            messages.error(request, "Username or Password was Incorrect!")
            return redirect('dashboard:login')
    return render(request, 'layout/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout Successfull.')
    return redirect('dashboard:login')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            form = PasswordResetForm({'email': user.email})
            if form.is_valid():
                form.save( request=request,
                    from_email='sohelsura777@gmail.com',
                    email_template_name='password_reset/password_reset_email.html')
                messages.success(request, 'Password reset email has been sent.')
            else:
                messages.error(request, 'Invalid email address.')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
        return redirect('dashboard:forgot_password')
    
    return render(request, 'password_reset/forgot_password.html')


def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                password1 = request.POST['password']

                user.password = make_password(password1)
                user.save()

                messages.success(request, 'Password has been reset successfully.')
                return redirect('dashboard:login')

            return render(request, 'password_reset/password_reset_confirm.html')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'Something went wrong. Please try again.')

    return redirect('dashboard:authentication_error')

def custom_404_error(request, exception=None):
    return render(request, '404.html', status=404)


@login_required
def dashboard_view(request):
    context = {
    }

    return render(request, 'layout/dashboard.html', context)

def product_list(request):
    products = Product.objects.all().order_by('sort_order')
    return render(request, 'product/product_list.html', {'products': products})

def product_add(request):
    if request.method == 'POST':
        # Handle form submission
        product = Product()
        product.name = request.POST.get('name')
        product.short_description = request.POST.get('short_description')
        product.description = request.POST.get('description')
        product.meta_title = request.POST.get('meta_title')
        product.meta_description = request.POST.get('meta_description')
        product.meta_keywords = request.POST.get('meta_keywords')
        product.sort_order = request.POST.get('sort_order')
        if request.FILES.get('image'):
            product.image = request.FILES['image']
        product.save()
        return redirect('dashboard:product_list')
    return render(request, 'product/product_form.html')

def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        # Handle form submission
        product.name = request.POST.get('name')
        product.short_description = request.POST.get('short_description')
        product.description = request.POST.get('description')
        product.meta_title = request.POST.get('meta_title')
        product.meta_description = request.POST.get('meta_description')
        product.meta_keywords = request.POST.get('meta_keywords')
        product.sort_order = request.POST.get('sort_order')
        if request.FILES.get('image'):
            product.image = request.FILES['image']
        product.save()
        return redirect('dashboard:product_list')
    return render(request, 'product/product_form.html', {'product': product})

@require_POST
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return JsonResponse({'status': 'success'})



def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blog/blog_list.html', {'blogs': blogs})

def blog_add(request):
    if request.method == 'POST':
        # Handle form submission
        blog = Blog()
        blog.title = request.POST.get('title')
        blog.short_description = request.POST.get('short_description')
        blog.description = request.POST.get('description')
        blog.meta_title = request.POST.get('meta_title')
        blog.meta_description = request.POST.get('meta_description')
        blog.meta_keywords = request.POST.get('meta_keywords')
        if request.FILES.get('image'):
            blog.image = request.FILES['image']
        blog.save()
        return redirect('dashboard:blog_list')
    return render(request, 'blog/blog_form.html')

def blog_edit(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        # Handle form submission
        blog.title = request.POST.get('title')
        blog.short_description = request.POST.get('short_description')
        blog.description = request.POST.get('description')
        blog.meta_title = request.POST.get('meta_title')
        blog.meta_description = request.POST.get('meta_description')
        blog.meta_keywords = request.POST.get('meta_keywords')
        if request.FILES.get('image'):
            blog.image = request.FILES['image']
        blog.save()
        return redirect('dashboard:blog_list')
    return render(request, 'blog/blog_form.html', {'blog': blog})

@require_POST
def blog_delete(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    blog.delete()
    return JsonResponse({'status': 'success'})

def contact_list(request):
    contacts = Contact.objects.all().order_by('-id')
    return render(request, 'contact_list.html', {'contacts': contacts})

@require_POST
def contact_delete(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    contact.delete()
    return JsonResponse({'status': 'success'})

def product_enquiry_list(request):
    enquiries = ProductEnquiry.objects.all().select_related('product')
    return render(request, 'product_enquiry_list.html', {'enquiries': enquiries})

@require_POST
def product_enquiry_delete(request, enquiry_id):
    enquiry = get_object_or_404(ProductEnquiry, id=enquiry_id)
    enquiry.delete()
    return JsonResponse({'status': 'success'})

def backup_database(request):
    database_settings = settings.DATABASES['default']
    db_name = database_settings['NAME']
    db_user = database_settings['USER']
    db_password = database_settings['PASSWORD']
    media_root = settings.MEDIA_ROOT

    d_drive_path = 'D:\\College Fees Backup' 
    backup_file = os.path.join(d_drive_path, f'{db_name}_backup.sql')
    # backup_file = os.path.join(media_root, f'{db_name}_backup.sql')

    mysqldump_path = r'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe'

    try:
        subprocess.run(
            [mysqldump_path, '-u', db_user, f'--password={db_password}', db_name],
            stdout=open(backup_file, 'w'),
            stderr=subprocess.PIPE,
            check=True
        )
        messages.success(request, f'Successfully backed up database to {backup_file}')
        return redirect('dashboard:dashboard')
    except subprocess.CalledProcessError as e:
        messages.error(request, f'Error while creating database backup: {e.stderr}')
        return redirect('dashboard:dashboard')