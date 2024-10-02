from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.email})"

class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products', null=True , blank=True)
    short_description = models.TextField(null=True)
    description = models.TextField(null=True)
    meta_title = models.CharField(max_length=255, null=True)
    meta_description = models.CharField(max_length=555, null=True)
    meta_keywords = models.CharField(max_length=555, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    sort_order = models.IntegerField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class ProductEnquiry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    contact = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name     

    class Meta:
        ordering = ['-created_at']  
    
class Blog(models.Model):
    title = models.CharField(max_length=555)
    image = models.ImageField(upload_to='blogs', null=True , blank=True)
    short_description = models.TextField(null=True)
    description = models.TextField(null=True)
    meta_title = models.CharField(max_length=555, null=True)
    meta_description = models.CharField(max_length=555, null=True)
    meta_keywords = models.CharField(max_length=555, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class MetaTag(models.Model):
    page = models.CharField(max_length=200, unique=True, help_text="Enter the name of the page (e.g., 'home', 'about').")
    title = models.CharField(max_length=200, help_text="Enter the title for the page.")
    description = models.TextField(help_text="Enter the description for the page.")
    keywords = models.CharField(max_length=200, help_text="Enter the keywords for the page (comma-separated).")
    og_title = models.CharField(max_length=200, help_text="Enter the open graph title for the page.")
    og_description = models.TextField(help_text="Enter the open graph description for the page.")

    def __str__(self):
        return self.page

    def get_absolute_url(self):
        return reverse(self.page)