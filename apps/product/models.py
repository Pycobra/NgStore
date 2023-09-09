from django.urls import reverse
from django.template.context_processors import request
from django.core.files import File
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models import Q
from django.db.models.signals import pre_save
from django.utils.text import slugify

from apps.vendor.models import Vendor
from apps.account.models import UserBase

from io import BytesIO
from PIL import Image  # NOQA
import uuid



class Category(MPTTModel):
    """
    Category Table implementated with MPTT
    """
    name = models.CharField( verbose_name=_("Category Name"), help_text=_("Required and unique"), max_length=255)
    slug = models.SlugField(verbose_name=_("Category safe url"), max_length=255)
    parent = TreeForeignKey("self", related_name='children', blank=True, null=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]
    class Meta:
        """enforcing that there can not be two categories under a parent with same slug
        unique_together = ('slug', 'parent',)"""
        verbose_name =_("Category")
        verbose_name_plural = _("Categories")
    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])

    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i + 1]))
        return slugs


    def get_absolute_url(self):
        return reverse('product_:category_list', args=[self.slug])

class ProductType(models.Model):
    """
    ProductType Table ll provide a list of the different types
    of products that are for sale.
    """
    name = models.CharField(verbose_name=_("Product Name"), help_text=_("Required"), max_length=255, unique=True)
    is_active = models.BooleanField(default=True)


    class Meta:
        verbose_name =_("Product Type")
        verbose_name_plural = _("Product Types")
    def __str__(self):
        return self.name

class ProductSpecification(models.Model):
    """
    ProductSpecification Table ll contain Product Specification
     or features for the product types.
    """
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT, related_name='prod_spec')
    name = models.CharField(verbose_name=_("Name"), help_text=_("Required"), max_length=255, unique=True)
    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")
    def __str__(self):
        return self.name

class Product(models.Model):
    product_type = models.ForeignKey(ProductType, related_name='vendors_product_type', on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, related_name='product_category', on_delete=models.RESTRICT)
    vendor = models.ForeignKey(Vendor, related_name='vendors_products', on_delete=models.RESTRICT)
    title = models.CharField(verbose_name=_("title"), help_text=_("Required"), max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(verbose_name=_("description"), help_text=_("Not Required"), blank=True)
    price = models.IntegerField(verbose_name=_("Regular price"), help_text=_("Maximum 999.99"),
                                error_messages={
                                    "name": {"max_length": _("The price must be between 0 and 999.99.")},
                                })
    discount_price = models.IntegerField(verbose_name=_("Discount price"), help_text=_("Maximum 999.99"),
                                error_messages={
                                    "name": {"max_length": _("The price must be between 0 and 999.99.")},
                                })
    discount_percent = models.IntegerField(verbose_name=_("Discount percent"), null=True)
    price_difference = models.IntegerField(verbose_name=_("Price difference"), null=True)
    in_stock = models.BooleanField(verbose_name=_("Product availability"), help_text=_("Change product availability"), default=True)
    is_active = models.BooleanField(verbose_name=_("Product visibility"), help_text=_("Change product visibility"), default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    users_wishlist = models.ManyToManyField(UserBase, related_name="user_wishlist", blank=True)
    likes = models.ManyToManyField(UserBase, related_name="likes", blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name =_("Product")
        verbose_name_plural = _("Products")
    def __str__(self):
        return self.title

    def get_cat_list(self):
        k = self.category

        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]

    def get_absolute_url(self):
        return reverse('product_:product_detail_', args=[self.category, self.slug])


def presaver(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.title)
    if instance.discount_price:
        new = ((int(instance.discount_price) / int(instance.price)) * 100)
        discount_percent = (100 - new)
        price_difference = (int(instance.price) - int(instance.discount_price))
        instance.discount_percent = discount_percent
        instance.price_difference = price_difference

pre_save.connect(presaver, sender=Product)

class ProductSpecificationValue(models.Model):
    """
    ProductSpecification value Table holds each of the Product
    individual Specification or bespoke features.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_in_spec')
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT, related_name='product_spec')
    value = models.CharField(verbose_name=_("Value"),
                             help_text=_("Product specificication value (maximum of 255 words)"),
                             max_length=255)
    class Meta:
        verbose_name =_("Product Specification Value")
        verbose_name_plural = _("Product Specifications Values")
    def __str__(self):
        return self.value

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    images = models.ImageField(verbose_name=_("image"),
                               help_text=_("Upload a product image"),
                               upload_to="images/uploads/", default="images/others/igor-lypnytskyi-PobecUzsK4c-unsplash.png")
    thumbnail = models.ImageField(upload_to='images/uploads/', default="images/others/igor-lypnytskyi-PobecUzsK4c-unsplash.png")
    alt_text = models.CharField(verbose_name=_("Alternative text"),
                             help_text=_("Please add alternative text"),
                             max_length=255)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name =_("Product Image")
        verbose_name_plural = _("Product Images")

    def get_thumbnail(self):
        #if d account already has a thumbnail
        if self.thumbnail:
            return self.thumbnail.url
        # if d account dont have a thumbnail
        else:
            if self.images:
                self.thumbnail = self.make_thumbnail(self.images)
                self.save()

                return self.thumbnail.url
            #thumbnail place holder
            else:
                return 'images/others/igor-lypnytskyi-PobecUzsK4c-unsplash.png'
    def make_thumbnail(self, images, size=(10, 10)):
        images=Image.open(images)
        images.convert('RGB')
        images.thumbnail(size)

        thumb_io =BytesIO()
        images.save(thumb_io, 'JPEG', quality=85)
        thumbnail=File(thumb_io, name=images.name)
        return thumbnail


class Comments(MPTTModel):
    made_by = models.ForeignKey(UserBase, related_name='commentator', null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    default_image = models.ImageField(default="images/others/igor-lypnytskyi-PobecUzsK4c-unsplash.png")
    made_on = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    parent = TreeForeignKey("self", related_name='children', blank=True, null=True, on_delete=models.CASCADE)
    content =  models.TextField(max_length=255)
    made_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering=['-made_at']

    def __str__(self):
        return self.made_on.title

















"""class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    ordering = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'categories of Product'
        ordering=['ordering']

    #dunder
    #to make this the models name at admin area || and how to reference this model
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_:category_list', args=[self.slug])

class ProductManagerAllView(models.Manager):
    def get_query_set(self):
        return super(ProductManagerAllView, self).get_queryset().filter(is_active=True, in_stock=True)
class ProductManagerSearchView(models.Manager):
    def get_query_set(self):
        query = request.GET.get('query', '')
        return super(ProductManagerSearchView, self).get_queryset().filter(Q(title__icontains=query) | Q(description__icontains=query))

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='categorys_related_name', on_delete=models.CASCADE)# video used category
    vendor = models.ForeignKey(Vendor, related_name='vendors_related_name', on_delete=models.CASCADE)# video used vendors
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    objects = models.Manager()
    product_manager = ProductManagerAllView()
    #product_id = models.CharField(max_length=255)
    #discount = models.BooleanField(default=False)
    #date_created = models.DateTimeField(auto_now_add=True)
    #date_modified = models.DateTimeField(auto_now=True)
    #in_stock = models.BooleanField(default=True)
    #is_active = models.BooleanField(default=False)
    #image = models.ImageField(upload_to='images/uploads/', default='images/uploads/fashion/waldo-kleyn-2bMHWCLfqRs-unsplash.png')
    #thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    # objects = models.Manager()           999(max_digits=6, decimal_places=2) 1000000000(max_digits=19, decimal_places=10)
    # produce = ProductManagerAllView()
    # search = ProductManagerSearchView()#i did dis class myself


    class Meta:
        verbose_name_plural = 'Products In Store'
        ordering=['-date_added']

    #dunder
    #to make this the models name at admin area || and how to reference this model
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_:product_detail_', args=[self.category, self.slug])"""

