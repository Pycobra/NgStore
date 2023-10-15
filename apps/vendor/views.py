from decimal  import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from django.forms import inlineformset_factory, modelformset_factory
from django.db.models import Q
from django.core import serializers
from django.contrib.sites.shortcuts import get_current_site

from apps.account.models import UserBase
from apps.product.models import Product, Category, ProductSpecificationValue, ProductImages
from apps.account.forms import RegistrationForm, ProfileEditForm
from apps.product.forms import AddCategoryForm
from apps.product.views import product_detail
from apps.cart.cart import Cart
from apps.communication.models import Messages


from .models import Vendor, Follow
from .forms import (ProductForm, ProductSpecForm, ProductImageForm, ProductImageForm2,
                    VendorRegistrationForm, VendorEditForm)


@login_required
def become_vendor(request):
    if request.user.is_authenticated:
        #ImageFormSet = modelformset_factory(VendorImageValue, form=VendorImageForm, extra=2)
        if request.user.is_vendor == False:
            if request.method == "POST":
                form = VendorRegistrationForm(request.POST, request.FILES)
                if form.is_valid():
                    userbase = UserBase.objects.get(user_name=request.user)
                    userbase.is_vendor = True
                    userbase.save()

                    vendor = form.save(commit=False)
                    vendor.vendor_image  = form.cleaned_data['vendor_image']
                    vendor.created_by  = userbase
                    vendor.is_active = True
                    vendor.save()

                    return redirect('vendor_:vendor_admin_', vendor.unique_id )
            else:
                form=VendorRegistrationForm()
            return render(request, 'vendor/become_vendor.html', {'form':form})
        else:
            return redirect('core_:frontpage')
    else:
        return redirect('account_:register')


@login_required
def follow_unfollow(request):
    if request.POST.get('action') == 'post':
        vendor_id = request.POST.get('vendor_id')
        follower = request.user
        following = Vendor.objects.get(id=vendor_id)
        already_follow = Follow.objects.filter(follower=follower, following=following)
        if already_follow:
            response = JsonResponse({'message':f"you have unfollowed {following.store_name} store", "followers_no":already_follow.count(),'exists':True})
            Follow.objects.get(follower=follower, following=following).delete()

        else:
            response = JsonResponse({'message':f"you are now following {following.store_name} store", "followers_no":already_follow.count(),'exists':False})
            follow = Follow.objects.create(follower=follower, following=following)
            follow.save()
    return response


@login_required
def vendor_admin(request, unique_id):
    vendor = get_object_or_404(Vendor, unique_id=unique_id)
    vendor_categories = Category.objects.filter(level=0)
    all_vendor = Vendor.objects.all().exclude(unique_id=unique_id)
    all_vendor2 = Vendor.objects.all()
    unread_msg = Messages.objects.filter(reciever_id_unique=unique_id, is_seen=False).count()
    am_following = Follow.objects.filter(follower=request.user)
    my_followers = {}
    if request.user.is_vendor:
        my_followers = Follow.objects.filter(following=request.user.which_vendor)
    stores_user_follow=[]
    for store in all_vendor2:
        for followers in am_following:
            if followers.following == store:
                stores_user_follow.append(followers.following)
    return render(request, 'vendor/vendor_dashboard.html', {'vendor':vendor, 'unread_msg':unread_msg, 'stores_user_follow':stores_user_follow,
                                                                'vendor_categories':vendor_categories, 'all_vendor':all_vendor,
                                                            'my_followers':my_followers, 'am_following': am_following})


@login_required
def vendor_admin2(request, vendor_id, category_slug):
    vendor = Vendor.objects.get(unique_id=vendor_id)
    vendor_categories = Category.objects.filter(level=0)
    all_vendor = Vendor.objects.all().exclude(unique_id=vendor.unique_id)
    unread_msg = Messages.objects.filter(reciever_id_unique=vendor.unique_id, is_seen=False).count()
    am_following = Follow.objects.filter(follower=request.user)
    my_followers = Follow.objects.filter(following=request.user.which_vendor)
    stores_user_follow=[]
    for store in all_vendor:
        for followers in am_following:
            if followers.following == store:
                stores_user_follow.append(followers.following)
    instance = Category.objects.get(slug=category_slug)
    product = Product.objects.filter(
        category__in=Category.objects.get(name=instance.name).get_descendants(include_self=True), vendor=vendor)
    return render(request, 'vendor/vendor_dashboard2.html', {'vendor':vendor, 'unread_msg':unread_msg, 'vendor_product': product,
                                                                'vendor_categories':vendor_categories, 'all_vendor':all_vendor,
                                                             'my_followers': my_followers})



@login_required
def vendor_admin_ajax(request):
    if request.POST.get('action') == 'post':
        query = request.POST.get('query')
        vendors = Vendor.objects.filter(Q(store_name__icontains=query))
        am_following = Follow.objects.filter(follower=request.user)

        serialized_queryset = serializers.serialize('python', vendors)

        for vend in vendors:
            for i in vend.vendor_image.all():
                image = i.image_value.images.url

        item = {}
        item['stores_user_follow'] = False
        for followers in am_following:
            if followers.following == vendors:
                item['stores_user_follow'] = True
        item['table'] = serialized_queryset

        response = JsonResponse({'item': item, 'image': image})
    return response



@login_required
def add_product(request):
    vendor = request.user.which_vendor
    ProductSpecFormSet = modelformset_factory(ProductSpecificationValue, form=ProductSpecForm, extra=3)
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        product_spec_form = ProductSpecFormSet(request.POST, request.FILES, queryset=ProductSpecificationValue.objects.none())
        product_img_form = ProductImageForm(request.POST, request.FILES)
        print("product_form.errors")
        print(product_form.errors)
        if product_form.errors:
            for field in product_form:
                if field.errors:
                    print(field.errors)
        if product_form.is_valid() and product_spec_form.is_valid() and product_img_form.is_valid:
            product_form = product_form.save(commit=False)
            product_form.vendor = vendor
            product_form.save()
            for form in product_spec_form.cleaned_data:
                # this will not allow site crash if the user do not upload all the spec fields
                if form:
                    specification = form['specification']
                    value = form['value']
                    spec = ProductSpecificationValue(product=product_form, specification=specification, value=value)
                    spec.save()

            for img in request.FILES.getlist('images'):
                if img == request.FILES.getlist('images')[0]:
                    ProductImages.objects.create(product=product_form, images=img, alt_text=slugify(product_form.title), is_main=True)
                else:
                    ProductImages.objects.create(product=product_form, images=img, alt_text=slugify(product_form.title) )


        return redirect('vendor_:vendor_admin_', vendor.unique_id)
    else:
        product_form=ProductForm()
        product_spec_form = ProductSpecFormSet(queryset=ProductSpecificationValue.objects.none())
        #product_img_form = ProductImageForm()
    return render(request,'vendor/add_product.html', {'product_form':product_form,
                          'product_spec_form':product_spec_form})#, 'product_img_form':product_img_form})


@login_required
def edit_product(request, id):
    vendor = request.user.which_vendor
    product = get_object_or_404(Product, id=id)
    ProductImageFormSet = inlineformset_factory(Product, ProductImages, form=ProductImageForm2, extra=0, can_delete=True)
    ProductSpecFormSet = inlineformset_factory(Product, ProductSpecificationValue, form=ProductSpecForm, can_delete=True)

    product_img_form2 = ProductImageFormSet(instance=product)
    cnt = 0
    for i in product_img_form2:
        cnt += 1
    print(cnt)
    if cnt == 0:
        ProductImageFormSet = inlineformset_factory(Product, ProductImages, form=ProductImageForm2, extra=5,can_delete=True)
        ProductSpecFormSet = inlineformset_factory(Product, ProductSpecificationValue, form=ProductSpecForm, extra=5,can_delete=True)
    elif cnt == 1:
        ProductImageFormSet = inlineformset_factory(Product, ProductImages, form=ProductImageForm2, extra=4,can_delete=True)
        ProductSpecFormSet = inlineformset_factory(Product, ProductSpecificationValue, form=ProductSpecForm,extra=4, can_delete=True)
    elif cnt == 2:
        ProductImageFormSet = inlineformset_factory(Product, ProductImages, form=ProductImageForm2, extra=3,can_delete=True)
        ProductSpecFormSet = inlineformset_factory(Product, ProductSpecificationValue, form=ProductSpecForm,extra=3, can_delete=True)
    elif cnt == 3:
        ProductImageFormSet = inlineformset_factory(Product, ProductImages, form=ProductImageForm2, extra=2,can_delete=True)
        ProductSpecFormSet = inlineformset_factory(Product, ProductSpecificationValue, form=ProductSpecForm,extra=2, can_delete=True)
    elif cnt == 4:
        ProductImageFormSet = inlineformset_factory(Product, ProductImages, form=ProductImageForm2, extra=1,can_delete=True)
        ProductSpecFormSet = inlineformset_factory(Product, ProductSpecificationValue, form=ProductSpecForm,extra=1, can_delete=True)


    if request.method == "POST":
        product_form = ProductForm(request.POST or None, instance=product)
        product_spec_form = ProductSpecFormSet(data=request.POST or None, instance=product)
        product_img_form = ProductImageFormSet(request.POST or None, request.FILES or None, instance=product)
        if product_form.is_valid() and product_spec_form.is_valid() and product_img_form.is_valid():
            product_form = product_form.save(commit=False)
            product_form.vendor = vendor
            product_form.save()
            product_spec_form.save()
            product_img_form.save()

            return product_detail(request, product.category.slug, product.slug)
        #     'set' object has no attribute 'append' 'QuerySet' object has no attribute 'pk'c
    else:
        product_form = ProductForm(instance=product)
        product_img_form = ProductImageFormSet(instance=product)
        product_spec_form = ProductSpecFormSet(instance=product)
    return render(request, 'vendor/edit_product.html', {'product': product, 'product_form': product_form,
                                                        'product_spec_form': product_spec_form,
                                                        'product_img_form': product_img_form})

@login_required
def delete_product(request):
    if request.POST.get('action') == 'post':
        id = request.POST.get('id')
        product = Product.objects.get(id=id, vendor=request.user.which_vendor)
        product.is_active = False
        product.save()
    response = JsonResponse({})
    return response

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


@login_required
def edit_vendor(request):
    vendor = request.user.which_vendor
    if request.method == "POST":
        vendor_form = VendorEditForm(request.POST or None, request.FILES or None, instance=vendor)
        if vendor_form.is_valid():
            user=vendor_form.save(commit=False)
            user.save()
            return redirect('vendor_:vendor_admin_', vendor.unique_id)
    else:
        vendor_form = VendorEditForm(instance=vendor)
    return render(request, 'vendor/edit_vendor.html', {'form':vendor_form})

def vendors_list(request):
    #gets all d vendors in Vendor models
    vendors = Vendor.objects.all()
    return render(request,'vendor/site_vendors.html', {'site_vendors':vendors})


def vendor_store(request, unique_id):
    vendor = get_object_or_404(Vendor, unique_id=unique_id)
    vendor_categories = Category.objects.filter(level=0)
    all_vendor = Vendor.objects.all().exclude(unique_id=unique_id)
    all_vendor2 = Vendor.objects.all()
    unread_msg = Messages.objects.filter(reciever_id_unique=unique_id, is_seen=False).count()
    am_following = Follow.objects.filter(follower=request.user)
    my_followers = {}
    if request.user.is_vendor:
        my_followers = Follow.objects.filter(following=request.user.which_vendor)
    stores_user_follow=[]
    for store in all_vendor2:
        for followers in am_following:
            if followers.following == store:
                stores_user_follow.append(followers.following)
    print(vendor)
    print(all_vendor)
    print(am_following)
    print(stores_user_follow)

    return render(request, 'vendor/vendor_dashboard.html', {'vendor': vendor, 'unread_msg':unread_msg, 'stores_user_follow':stores_user_follow,
                                                            'vendor_categories': vendor_categories, 'all_vendor':all_vendor,
                                                            'my_followers':my_followers})


def suscribe_to_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    subscription_type=vendor.vendor_subscription_type.all()
    return render(request, 'vendor/suscribe_to_vendor.html', {'subscription_type':subscription_type, 'vendor':vendor})

@login_required
def suscribe_package(request):
    response = ""
    users_store = False
    if request.POST.get('action') == 'post':
        subscription_id = request.POST.get('subscription_id')
        user_subscription = SubscriptionType.objects.get(id=subscription_id)
        subscription=Subscriptions.objects.filter(suscriber=request.user, vendor=user_subscription.vendor,
                                     subscription_plan=user_subscription)
        if request.user.is_vendor:
            #wont allow u add d suscription if the current logged in user store owns that suscribe_package
            if (user_subscription.vendor == request.user.which_vendor):
                users_store = True
        #wont allow u add d suscription if the current logged in user is already suscribed to that package
        if subscription.exists():
            messages.success(request, "your subscription to this package has not expired")
            #msg="your subscription to this package has not expired"
        if not subscription.exists() and not users_store:
            Subscriptions.objects.create(suscriber=request.user, vendor=user_subscription.vendor,
                                     subscription_plan=user_subscription)
            messages.success(request, "subscription successfull")
            #msg="subscription successfull"
        #response = JsonResponse({'msg':msg})



def sell(request):
    return render(request,'vendor/sellonngstoreboy.html')















