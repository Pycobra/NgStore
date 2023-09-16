from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required


from apps.product.models import Product, Category
from apps.vendor.models import Vendor, Follow




def frontpage(request):
    # use line 8 > where there multiple values to b goten such as images which means we query db more than once, so we query db just once
    all_products = Product.objects.prefetch_related("product_images").filter(is_active=True, in_stock=True).order_by('-created_at')
    categories = Category.objects.filter(level=0)
    return render(request, 'core/frontpage.html', {'all_products': all_products, 'categories':categories})

def contact(request):
    return render(request, 'core/contact.html')

def category_search(request, category):
    query = category
    print(query)
    product = Product.objects.filter(Q(category__slug=query))

    #product = Product.objects.all()
    #product = Product.objects.filter(Q(category__name__icontains=query))
    brands = Product.objects.filter(is_active=True, in_stock=True)[:9]

    return render(request, 'product/search.html', {'product_search': product, 'product_search_query': query
                                                   , 'brands':brands})
"""
baby-products
computing
electronics
fashion
health-and-beauty
home-and-office
mobiles
sport
toy-and-games

Sporting
Health & Beauty
Mobiles
Fashion > women
Fashion > children > Shirts
Baby Products
Computing > Keyboard
Fashion > children
"""
