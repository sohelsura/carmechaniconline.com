from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from carmechaniconline import settings
from main.forms import ProductEnquiryForm
from main.models import Blog, Contact, Product, MetaTag
from django.views.generic import ListView, DetailView
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic import TemplateView

# Create your views here.
def index(request):
    latest_blogs = Blog.objects.order_by('-created_at')[:3]
    services = Product.objects.all().order_by('sort_order')[:8]  # Limit to 8 products
    total_services = services.count()
    
    if total_services <= 6:
        left_services = services[:3]
        right_services = services[3:]
    else:
        # For 7 or 8 products, distribute evenly
        mid_point = total_services // 2
        left_services = services[:mid_point]
        right_services = services[mid_point:]

    context = {
        'latest_blogs': latest_blogs,
        'blog_description': "Explore our latest blog posts covering various topics and insights.",
        'left_services': left_services,
        'right_services': right_services,
        'services' : services
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html', {})

def terms_condition(request):
    return render(request, 'terms-policy.html', {})

def privacy_policy(request):
    return render(request, 'privacy-policy.html', {})

def cancellation_policy(request):
    return render(request, 'cancellation-refund-policy.html', {})

class BlogListView(ListView):
    model = Blog
    template_name = 'blog.html'
    context_object_name = 'blogs'
    paginate_by = 6  # Show 6 blogs per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog_description'] = "Explore our latest blog posts covering various topics and insights."
        return context
    
class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog-detail.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()
        context['recent_posts'] = Blog.objects.exclude(id=self.object.id).order_by('-created_at')[:5]
        context['archive_dates'] = Blog.objects.dates('created_at', 'month', order='DESC')
        return context

class ProductListView(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all().order_by('sort_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_description'] = "Discover our diverse range of products designed to meet your needs. Quality and innovation in every item."
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product-detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['form'] = ProductEnquiryForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ProductEnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.product = self.object
            enquiry.save()
            messages.success(request, "Your enquiry has been submitted successfully.")
            return redirect('product-detail', slug=self.object.slug)
        else:
            context = self.get_context_data(object=self.object)
            context['form'] = form
            return self.render_to_response(context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact = Contact(name=name, email=email, phone_number=phone, subject=subject, message=message)
        contact.save()

        # company_subject = f"New Contact Form Submission: {subject}"
        # company_message = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nSubject: {subject}\nMessage: {message}"
        
        # send_mail(
        #     company_subject,
        #     company_message,
        #     settings.DEFAULT_FROM_EMAIL,
        #     [settings.COMPANY_EMAIL],
        #     fail_silently=False,
        # )

        # user_subject = "Thank you for contacting Car Mechanic Online"
        # html_message = render_to_string('emails/autoresponse.html', {'name': name})
        # plain_message = strip_tags(html_message)
        
        # email = EmailMultiAlternatives(
        #     user_subject,
        #     plain_message,
        #     settings.DEFAULT_FROM_EMAIL,
        #     [email]
        # )
        
        # email.attach_alternative(html_message, "text/html")
        # email.send()

        messages.success(request, 'Your message was sent successfully.')
        return redirect('main:contact')
    return render(request, 'contact.html', {})

class RobotsTxtView(TemplateView):
    template_name = "robots.txt"
    

    