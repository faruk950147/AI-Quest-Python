from django.db import models
from django.utils.text import slugify
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

# ------------------- IMAGE TAG MIXIN -------------------
class ImageTagMixin:
    def image_tag(self, image_field, width=50, height=50):
        image = getattr(self, image_field, None)
        if image and hasattr(image, 'url'):
            return mark_safe(f'<img src="{image.url}" width="{width}" height="{height}" />')
        return mark_safe('<span>No Image Available</span>')

# ------------------- CATEGORY MODEL -------------------
class Category(models.Model, ImageTagMixin):
    class CategoryType(models.TextChoices):
        NONE = 'NONE', 'None'
        LEHENGA = 'LEHENGA', 'Lehenga'
        SHAREE = 'SHAREE', 'Sharee'
        GENT_PANTS = 'GENT_PANTS', 'Gent Pants'
        BORKHA = 'BORKHA', 'Borkha'
        BABY_FASHION = 'BABY_FASHION', 'Baby Fashion'

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        INACTIVE = 'INACTIVE', 'Inactive'

    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True)
    category_type = models.CharField(max_length=50, choices=CategoryType.choices, default=CategoryType.NONE)
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True)
    keyword = models.CharField(max_length=150, default='N/A', blank=True)
    description = models.CharField(max_length=150, default='N/A', blank=True)
    image = models.ImageField(upload_to='categories/%Y/%m/%d/')
    status = models.CharField(max_length=8, choices=Status.choices, default=Status.ACTIVE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = '01. Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def image_preview(self):
        return self.image_tag('image', width=100, height=100)

    def __str__(self):
        return f'{self.title} - {self.get_status_display()}'

# ------------------- BRAND MODEL -------------------
class Brand(models.Model, ImageTagMixin):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        INACTIVE = 'INACTIVE', 'Inactive'

    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True)
    keyword = models.CharField(max_length=150, default='N/A')
    description = models.CharField(max_length=150, default='N/A')
    image = models.ImageField(upload_to='brands/%Y/%m/%d/')
    status = models.CharField(max_length=8, choices=Status.choices, default=Status.ACTIVE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = '02. Brands'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Brand.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def image_preview(self):
        return self.image_tag('image', width=50, height=50)

    def __str__(self):
        return f'{self.title} - {self.get_status_display()}'

# ------------------- PRODUCT MODEL -------------------
class Product(models.Model, ImageTagMixin):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        INACTIVE = 'INACTIVE', 'Inactive'

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True)
    old_price = models.DecimalField(decimal_places=2, max_digits=10, default=1000.00)
    sale_price = models.DecimalField(decimal_places=2, max_digits=10, default=500.00)
    available_stock = models.PositiveIntegerField(validators=[MaxValueValidator(50)], default=0)
    discount_percent = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    keyword = models.TextField(default='N/A')
    description = models.TextField(default='N/A')
    image = models.ImageField(upload_to='products/%Y/%m/%d/')
    status = models.CharField(max_length=8, choices=Status.choices, default=Status.ACTIVE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = '03. Products'

    def save(self, *args, **kwargs):
        # Slug
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug

        # Discount calculation
        if self.old_price > 0:
            self.discount_percent = round((1 - self.sale_price / self.old_price) * 100)

        super().save(*args, **kwargs)

    def clean(self):
        if self.sale_price > self.old_price:
            raise ValidationError("Sale price cannot be greater than old price.")

    @property
    def image_preview(self):
        return self.image_tag('image', width=50, height=50)

    def __str__(self):
        return f'{self.title} - {self.get_status_display()}'

# ------------------- SLIDER MODEL -------------------
class Slider(models.Model, ImageTagMixin):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        INACTIVE = 'INACTIVE', 'Inactive'

    title = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to='sliders/%Y/%m/%d/')
    status = models.CharField(max_length=8, choices=Status.choices, default=Status.ACTIVE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = '04. Sliders'

    @property
    def image_preview(self):
        return self.image_tag('image', width=50, height=50)

    def __str__(self):
        return f'{self.title} - {self.get_status_display()}'
