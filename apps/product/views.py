import random
from decimal  import Decimal
from django.forms.models import model_to_dict

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers


from .models import Category, Product, ProductType, ProductSpecificationValue, Comments
from .forms import AddToCartForm, AddCategoryForm, ColorSearchForm

from apps.cart.cart import Cart
from apps.vendor.forms import ProductForm, VendorRegistrationForm, VendorEditForm
from apps.communication.forms import NewCommentForm
from apps.vendor.models import Follow


def show_category(request,hierarchy= None):
    category_slug = hierarchy.split('/')
    parent = None
    root = Category.objects.all()
    for slug in category_slug[:-1]:
        parent = root.get(parent=parent, slug = slug)
    instance = Category.objects.get(parent=parent,slug=category_slug[-1])
    product = Product.objects.filter(
        category__in=Category.objects.filter(name=instance.name).get_descendants(include_self=True))
    brands = ProductType.objects.all()
    return render(request, 'product/search.html', {'product_search': product, 'product_search_query': instance
                                                   , 'brands':brands})

def parent_child_check(request):
    if request.POST.get('mainAction') == 'post':
        id = request.POST.get('category_id')
        categories = Category.objects.filter(level=0)
        for i in categories:
            categories = Category.objects.get(id=i.id).get_descendants(include_self=True)
        response = JsonResponse({'categories': "rr"})
        return response

def product_all(request):
    products = Product.objects.prefetch_related("product_image").filter(is_active=True)
    return render(request, "store/product_all.html", {"products": products})

def search(request):
    query = request.GET.get('query', '')
    product = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    brands = ProductType.objects.all()

    return render(request, 'product/search.html', {'product_search': product, 'product_search_query': query
                                                   , 'brands':brands, 'color_input':ColorSearchForm})

def filter_page(request):
    if request.method == "GET":
        query = request.GET.get('query', '')
        query = query.split(',')
        discount_percent = []
        user_chose_spec = False
        """sizes = ['S','M','L','X','XL','XXL','Red','Blue','White','Black',
                 'Brown','Green','Yellow','Purple','Orange','Cream','Lemon']"""
        for i in query:
            if i == '< 10%':
                for num in range(1,10):
                    discount_percent.append(num)
            if i == '< 20%':
                for num in range(11,21):
                    discount_percent.append(num)
            if i == '< 30%':
                for num in range(21,31):
                    discount_percent.append(num)
            if i == '< 40%':
                for num in range(31,41):
                    discount_percent.append(num)
            if i == '< 50%':
                for num in range(41,51):
                    discount_percent.append(num)
            if i == '< 60%':
                for num in range(51,61):
                    discount_percent.append(num)

        brands = ProductType.objects.all()

        name_list = []
        for i in query:
            instance = Category.objects.filter(slug=i)
            if instance:
                for all in instance:
                    name_list.append(all.name)
        if 'has_category' in query and "has_brand" in query and "has_discount" in query:
            product = Product.objects.filter(Q(discount_percent__in=discount_percent, product_type__name__in=query,
                                               category__in=Category.objects.filter(name__in=name_list).get_descendants(include_self=True)))
        elif 'has_category' in query and "has_brand" in query:
            product = Product.objects.filter(Q(product_type__name__in=query,
                                               category__in=Category.objects.filter(name__in=name_list).get_descendants(include_self=True)))
        elif 'has_category' in query and "has_discount" in query:
            product = Product.objects.filter(Q(discount_percent__in=discount_percent,
                                               category__in=Category.objects.filter(name__in=name_list).get_descendants(include_self=True)))
        elif "has_brand" in query and "has_discount" in query:
            product = Product.objects.filter(Q(discount_percent__in=discount_percent, product_type__name__in=query))
        elif 'has_category' in query:
            product = Product.objects.filter(Q(category__in=Category.objects.filter(name__in=name_list).get_descendants(include_self=True)))
        elif "has_brand" in query:
            product = Product.objects.filter(Q(product_type__name__in=query))
        elif "has_discount" in query:
            product = Product.objects.filter(Q(discount_percent__in=discount_percent))

        if ('has_size' in query or 'has_color' in query):
            spec_list=[]
            if ('has_category' in query or "has_brand" in query or "has_discount" in query) and \
                    ('has_size' in query or 'has_color' in query):
                specification = ProductSpecificationValue.objects.filter(Q(product__in=product, value__in=query))
                for spec in specification:
                    spec_list.append(spec.product.id)

            if ('has_category' not in query and "has_brand" not in query and "has_discount" not in query) and \
                    ('has_size' in query or 'has_color' in query):
                specification = ProductSpecificationValue.objects.filter(Q(value__in=query))
                for spec in specification:
                    spec_list.append(spec.product.id)
            product = Product.objects.filter(Q(id__in=spec_list))
        if ('has_category' in query):
            query.remove('has_category')
        if ("has_brand" in query):
            query.remove("has_brand")
        if ("has_discount" in query):
            query.remove("has_discount")
        if ('has_size' in query):
            query.remove('has_size')
        if ('has_color' in query):
            query.remove('has_color')

        return render(request, 'product/filter_page.html', {'product_search': product, 'product_search_query': query
                                                       , 'brands':brands, 'user_chose_spec':user_chose_spec})

def search_brand(request):
    if request.GET.get('action') == 'get':
        brands = request.GET.get('brands')
        brands = ProductType.objects.filter(name__iexact=brands)

        item = {}
        if brands:
            serialized_queryset = serializers.serialize('python', brands)
            item['table'] = serialized_queryset

        response = JsonResponse({'item': item})
    return response

from django import template
register = template.Library()


#@register.simple_tag(takes_context=True)
@register.filter(is_safe=True)
def search_single(request):
    if request.method == "GET":
        query = request.GET.get('query', '')
        product_search = Product.objects.filter(Q(title__icontains=query) |
                        Q(description__icontains=query) | Q(id__icontains=query))
        brands = ProductType.objects.all()

        response = JsonResponse({'product_search': list(product_search)})
        return response

def search_single2(request):
    if request.GET.get('action') == 'get':
        query = request.GET.get('productID')
        product_search = Product.objects.filter(Q(title__icontains=query) |
                        Q(description__icontains=query) | Q(id__icontains=query)).values()
        brands = ProductType.objects.all()
        product = """
            <div class="box-body">
                {% for i in product_search %}
                <a href="{% url 'product_:product_detail_' i.category.slug i.slug %}"class="">
                    <div class="card">
                        {% for image in i.product_images.all %}
                        {% if image.is_main %}
                        <div class="card-img">
                            <span>10%</span>
                            <img src="{{ image.images.url }}" alt="{{ image.images.alt_text }}"
                        </div>
                        <div class="card-text">
                            <h2 class="subtitle"> {{i.description}} </h2>
                            <span> NGstoreboy Price Now</span>
                            <h3 class="price is-size-6 mb-5"> {{i.price}} </h3>
                            <h3 class="price is-size-6 mb-5"> {{i.discount_price}} </h3>
                            <button class="is-uppercase">ADD TO CART</button>
                        </div>
                        {% endif %}
                        {% endfor %}
                    </div>
                </a>
                {% endfor %}
            </div>"""
        response = JsonResponse({'product_search': list(product)})
        return response
def product_detail(request, category_slugz, product_slugz):
    cart = Cart(request)
    products = get_object_or_404(Product, category__slug=category_slugz, slug=product_slugz, is_active=True)
    stores_user_follow=[]
    for i in products.vendor.vendor_follower.all():
        stores_user_follow.append(i.follower)

    wishlist = products.users_wishlist.all().count()
    likes = products.likes.all().count()
    product_id = str(products.id)
    wishlist_boolean = False
    like_boolean = False
    product_spec = ProductSpecificationValue.objects.filter(product=products)

    #------------------------------------------------------
    allcomments = products.comments.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(allcomments, 10)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    if products.users_wishlist.filter(id=request.user.id).exists():
        wishlist_boolean=True
    if products.likes.filter(id=request.user.id).exists():
        like_boolean=True
    if request.method == 'POST':
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.post = products
            user_comment.save()
            return HttpResponseRedirect('/' + products.slug)

            return redirect('product_:product_detail_', category_slug= category_slugz, product_slug=product_slugz)
    else:
        comment_form = NewCommentForm()
        form = AddToCartForm()

    #----------------------------------------------------
    similar_products = list(products.category.product_category.exclude(id=products.id))
    if len(similar_products) >= 4:
        similar_products = random.sample(similar_products, 4)

    #-------------------------------------------------
    breadcrumbs_link = products.get_cat_list()
    category_name = [' '.join(i.split('/')[-1].split('-')) for i in breadcrumbs_link]
    breadcrumbs = zip(breadcrumbs_link, category_name)
    return render(request, 'product/product.html', {'comment_form': comment_form, 'product': products, 'product_id': product_id,
                                                    'wishlist': str(wishlist), 'wishlist_boolean':wishlist_boolean,
                                                    'likes': str(likes), 'like_boolean':like_boolean, 'allcomments':allcomments, 'comments':comments,
                                                    'product_spec':product_spec, 'stores_user_follow':stores_user_follow, 'breadcrumbs': breadcrumbs})


def make_comment(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('comment')
        product_id = request.POST.get('product_id')
        products = Product.objects.get_object_or_404get(id=product_id)
        wishlist = products.users_wishlist.all().count()
        likes = products.likes.all().count()
        product_id = str(products.id)
        wishlist_boolean = False
        like_boolean = False
        product_spec = ProductSpecificationValue.objects.filter(product=products)

        # ------------------------------------------------------
        if request.user.is_authenticated:
            Comments.objects.create(made_by=request.user,
                                    name=request.user.firstname + " " + request.user.surname,
                                    email=request.user.email, default_image=request.user.user_image,
                                    made_on=products, parent=None, content=comment)
        else:
            if not request.user.is_authenticated and name != "" and email != "":
                Comments.objects.create(made_by=None, name=name, email=request.user.email,
                                        made_on=products, parent=None, content=comment)
            else:
                error = "e no follo"

                response = JsonResponse({'comments': error})
                return response

        allcomments = products.comments.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(allcomments, 10)
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        if products.users_wishlist.filter(id=request.user.id).exists():
            wishlist_boolean = True
        if products.likes.filter(id=request.user.id).exists():
            like_boolean = True

        # ----------------------------------------------------
        similar_products = list(products.category.product_category.exclude(id=products.id))
        if len(similar_products) >= 4:
            similar_products = random.sample(similar_products, 4)

        # -------------------------------------------------
        breadcrumbs_link = products.get_cat_list()
        category_name = [' '.join(i.split('/')[-1].split('-')) for i in breadcrumbs_link]
        breadcrumbs = zip(breadcrumbs_link, category_name)


        comment_form = NewCommentForm()
        form = AddToCartForm()

        return render(request, 'product/product.html',
                      {'comment_form': comment_form, 'product': products, 'product_id': product_id,
                       'wishlist': str(wishlist), 'wishlist_boolean': wishlist_boolean,
                       'likes': str(likes), 'like_boolean': like_boolean, 'allcomments': allcomments,
                       'comments': comments,
                       'product_spec': product_spec, 'breadcrumbs': breadcrumbs})


def product_detail2(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        qtyAction = request.POST.get('qtyAction')
        productID = int(request.POST.get('productID'))
        productQTY = int(request.POST.get('productQTY'))
        if qtyAction == 'include_item':
            product = get_object_or_404(Product, id=productID)
            cart.add(product_id=productID, product=product, quantity=productQTY, update_quantity=False)
            messages.success(request, 'The account was successfully added to the account')
            response = JsonResponse(
                {'cart_length': cart.__len__()})
            return response

@login_required
def add_category(request):
    if request.user.is_superuser:
        if request.method == "POST":
            form = AddCategoryForm(request.POST)
            if form.is_valid():
                vendor = form.save(commit=False)
                title = form.cleaned_data['title']
                slug = form.cleaned_data['slug']
                Category.objects.create(title=title, slug=slug, ordering='1')
        else:
            form=AddCategoryForm()
        return render(request,'product/add_category.html', {'form':form})
    else:
        return redirect('core_:frontpage')

def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    return render(request, 'product/category.html', {'category_in_product_view': category})

def vendor_category(request):
    if request.GET.get('mainAction') == 'post':
        category_slug = request.GET.get('category_slug')
        category = get_object_or_404(Category, slug=category_slug)
        product = Product.objects.filter(
            Product, category__in=Category.objects.get(name=category_slug).get_descendants(include_self=True)
        )
        response = JsonResponse({'product': product})
        return response

@login_required
def likes_add_and_remove(request, id):
    if request.GET.get('action') == 'get':
        product = get_object_or_404(Product, id=id)
        if product.likes.filter(id=request.user.id).exists():
            product.likes.remove(request.user)
            product_exist = True
            action_text='<i class="fa fa-heart-o" id="icon2" style="color:var(--lightblue);"> like</i>'
        else:
            product.likes.add(request.user)
            product_exist = False
            action_text='<i class="fa fa-heart-o" id="icon2" style="color:var(--lightblue);"> unlike</i>'
        likes = product.likes.all().count()
        response = JsonResponse({'likes_no': str(likes), 'action_text':action_text, 'product_exist':product_exist})
        return response

@login_required
def remove_from_likes(request):
    if request.GET.get('action') == 'get':
        id = request.GET.get('productID')
        product = get_object_or_404(Product, id=id)
        product_count=product.likes.add(request.user).count()
        if product.likes.filter(id=request.user.id).exists():
            product.likes.remove(request.user)
            messages.success(request, "you have unliked " + product.title)
    response = JsonResponse({'product_count':product_count})
    return response

@login_required
def add_product(request):
    vendor = request.user.which_vendor
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)

            product.vendor = vendor
            product.title = product.title
            product.category = product.category
            product.slug = slugify(product.title)
            product.description = product.description
            product.price = Decimal(product.price)
            product.in_stock = True
            product.is_active = True
            product.save()
            return redirect('vendor_:vendor_admin_')
    else:
        form=ProductForm()
    return render(request,'vendor/add_product.html', {'form':form})

@login_required
def add_category(request):
    if request.user.is_superuser:
        if request.method == "POST":
            form = AddCategoryForm(request.POST)
            if form.is_valid():
                vendor = form.save(commit=False)
                title = vendor.cleaned_data['title']
                slug = vendor.cleaned_data['slug']
                Category.objects.create(title=title, slug=slug, ordering='1')
        else:
            form=AddCategoryForm()
        return render(request,'product/add_category.html', {'form':form})
    else:
        return redirect('core_:frontpage')
