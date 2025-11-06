from django.db import models
from django.utils.text import slugify
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

class CategoryType(models.Model):
    title = models.CharField(max_length=50, unique=True)
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='ACTIVE')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title


class Category(models.Model):
    parent = models.ForeignKey(
        'self', related_name='children', on_delete=models.CASCADE, null=True, blank=True
    )
    category_type = models.ForeignKey(
        CategoryType, on_delete=models.SET_NULL, null=True, blank=True
    )
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True)
    keyword = models.CharField(max_length=150, default='N/A', blank=True)
    description = models.CharField(max_length=150, default='N/A', blank=True)
    image = models.ImageField(upload_to='categories/%Y/%m/%d/')

    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='ACTIVE')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = '01. Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if Category.objects.filter(slug=self.slug).exists() and not self.id:
            self.slug = f'{self.slug}-{self.pk}'
        super().save(*args, **kwargs)

    @property
    def image_tag(self):
        return self.get_image_tag(self.image)

    def get_image_tag(self, image):
        if image and hasattr(image, 'url'):
            return mark_safe(f'<img src="{image.url}" width="100" height="100"/>')
        return mark_safe('<span>No Image Available</span>')

    def __str__(self):
        type_name = self.category_type.title if self.category_type else "No Type"
        return f'{self.title} - {type_name} - {"Active" if self.status=="ACTIVE" else "Inactive"}'


class Brand(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True)
    keyword = models.CharField(max_length=150, default='N/A')
    description = models.CharField(max_length=150, default='N/A')
    image = models.ImageField(upload_to='brands/%Y/%m/%d/')
    
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='ACTIVE')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = '02. Brands'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Ensure unique slug by appending an incremental number if it already exists
        if Brand.objects.filter(slug=self.slug).exists() and not self.id:
            self.slug = f'{self.slug}-{self.pk}'
        
        super().save(*args, **kwargs)

    @property
    def image_tag(self):
        return self.get_image_tag(self.image)

    def get_image_tag(self, image):
        if image and hasattr(image, 'url'):
            return mark_safe(f'<img src="{image.url}" width="50" height="50"/>')
        return mark_safe('<span>No Image Available</span>')

    def __str__(self):
        return f'{self.title} - {"Active" if self.status == "ACTIVE" else "Inactive"}'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True, null=True, blank=True)
    old_price = models.DecimalField(decimal_places=2, max_digits=10, default=1000.00)
    sale_price = models.DecimalField(decimal_places=2, max_digits=10, default=500.00)
    available_stock = models.PositiveIntegerField(validators=[MaxValueValidator(50)], default=0)
    discount_percent = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    keyword = models.TextField(default='N/A')
    description = models.TextField(default='N/A')
    image = models.ImageField(upload_to='products/%Y/%m/%d/')
    
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='ACTIVE')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = '03. Products'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Ensure unique slug by appending an incremental number if it already exists
        if Product.objects.filter(slug=self.slug).exists() and not self.id:
            self.slug = f'{self.slug}-{self.pk}'
        
        super().save(*args, **kwargs)

    def clean(self):
        if self.sale_price > self.old_price:
            raise ValidationError("Sale price cannot be greater than old price.")

    @property
    def image_tag(self):
        return self.get_image_tag(self.image)

    def get_image_tag(self, image):
        if image and hasattr(image, 'url'):
            return mark_safe(f'<img src="{image.url}" width="50" height="50"/>')
        return mark_safe('<span>No Image Available</span>')

    def __str__(self):
        return f'{self.title} - {"Active" if self.status == "ACTIVE" else "Inactive"}'


class Slider(models.Model):
    title = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to='sliders/%Y/%m/%d/')
    
    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='ACTIVE')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = '04. Sliders'

    @property
    def image_tag(self):
        return self.get_image_tag(self.image)

    def get_image_tag(self, image):
        if image and hasattr(image, 'url'):
            return mark_safe(f'<img src="{image.url}" width="50" height="50"/>')
        return mark_safe('<span>No Image Available</span>')

    def __str__(self):
        return f'{self.title} - {"Active" if self.status == "ACTIVE" else "Inactive"}'
