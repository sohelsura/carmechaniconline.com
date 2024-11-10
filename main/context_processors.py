from main.models import Blog, MetaTag, Product

def navbar_products(request):
    return {'products': Product.objects.all().order_by('sort_order')}

def meta_tags(request):
    meta = None

    try:
        meta = MetaTag.objects.get(page=request.resolver_match.url_name)
    except MetaTag.DoesNotExist:
        pass

    if meta is None:
        if 'slug' in request.resolver_match.kwargs:
            product_slug = request.resolver_match.kwargs['slug']
            try:
                product = Product.objects.get(slug=product_slug)
                meta = {
                    'title': product.meta_title,
                    'description': product.meta_description,
                    'keywords': product.meta_keywords,
                }
            except Product.DoesNotExist:
                pass
        elif 'slug' in request.resolver_match.kwargs:
            blog_slug = request.resolver_match.kwargs['slug']
            try:
                blog = Blog.objects.get(slug=blog_slug)
                meta = {
                    'title': blog.meta_title,
                    'description': blog.meta_description,
                    'keywords': blog.meta_keywords,
                }
            except Blog.DoesNotExist:
                pass

    return {'meta': meta}

# context_processors.py

def canonical_url(request):
    # Get the current path
    path = request.path.rstrip('/')
    
    # Build the full canonical URL
    protocol = 'https'  # Force HTTPS
    domain = 'www.carmechaniconline.com'  # Your domain
    canonical_url = f'{protocol}://{domain}{path}'
    
    return {
        'canonical_url': canonical_url
    }