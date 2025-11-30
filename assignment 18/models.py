from django.db import models
from django.utils.text import slugify
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Avg
from decimal import Decimal

User = get_user_model()

# =========================================================
# 01. CHOICES
# =========================================================
STATUS_CHOICES = (
    ('active', 'Active'),
    ('inactive', 'Inactive'),
)

SLIDER_TYPE_CHOICES = (
    ('none', 'None'),
    ('slider', 'Slider'),
    ('add', 'Add'),
    ('feature', 'Feature'),
    ('promotion', 'Promotion'),
)

# =========================================================
# 02. SLUG GENERATOR
# =========================================================
def generate_unique_slug(cls, title: str) -> str:
    base_slug = slugify(title)
    slug = base_slug
    counter = 1
    while cls.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug

# =========================================================
# 03. BASE MODEL
# =========================================================
class BaseModel(models.Model):
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    is_featured = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# =========================================================
# 04. IMAGE TAG MIXIN
# =========================================================
class ImageTagMixin(models.Model):
    class Meta:
        abstract = True

    def image_tag(self):
        img = getattr(self, 'image', None)
        if img and hasattr(img, 'url'):
            return mark_safe(f'<img src="{img.url}" style="max-width:50px; max-height:50px;" />')
        return mark_safe('<span>No Image</span>')

# =========================================================
# 05. CATEGORY MODEL
# =========================================================
class Category(BaseModel, ImageTagMixin):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE,
                               null=True, blank=True)
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    keyword = models.CharField(max_length=150, default='N/A')
    description = models.CharField(max_length=150, default='N/A')

    image = models.ImageField(upload_to='categories/%Y/%m/%d/', default='defaults/default.jpg')

    class Meta:
        ordering = ['id']
        verbose_name_plural = '01. Categories'

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.slug:
            self.slug = generate_unique_slug(Category, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

# =========================================================
# 06. BRAND MODEL
# =========================================================
class Brand(BaseModel, ImageTagMixin):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    keyword = models.CharField(max_length=150, default='N/A')
    description = models.CharField(max_length=150, default='N/A')

    image = models.ImageField(upload_to='brands/%Y/%m/%d/', default='defaults/default.jpg')

    class Meta:
        ordering = ['id']
        verbose_name_plural = '02. Brands'

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.slug:
            self.slug = generate_unique_slug(Brand, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

# =========================================================
# 07. PRODUCT MODEL
# =========================================================
class Product(BaseModel, ImageTagMixin):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    old_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    available_stock = models.PositiveIntegerField(validators=[MaxValueValidator(10000)], default=1)
    discount_percent = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)

    prev_des = models.TextField(default='N/A')
    add_des = models.TextField(default='N/A')
    short_des = models.TextField(default='N/A')
    long_des = models.TextField(default='N/A')
    keyword = models.TextField(default='N/A')
    description = models.TextField(default='N/A')
    tag = models.CharField(max_length=150, default='N/A')

    deadline = models.DateTimeField(blank=True, null=True)
    is_deadline = models.BooleanField(default=False)
    sold = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['id']
        verbose_name_plural = '03. Products'

    def save(self, *args, **kwargs):
        # Sale price auto calculation
        self.sale_price = (
            (self.old_price * (Decimal(100) - Decimal(self.discount_percent)) / Decimal(100))
            .quantize(Decimal('0.01'))
        )
        self.full_clean()
        if not self.slug:
            self.slug = generate_unique_slug(Product, self.title)
        super().save(*args, **kwargs)

    def clean(self):
        if self.deadline and self.deadline < timezone.now():
            raise ValidationError("Deadline cannot be in the past.")

    @property
    def remaining_seconds(self):
        if self.deadline and self.is_deadline:
            now = timezone.now()
            remaining = self.deadline - now
            return max(0, int(remaining.total_seconds()))
        return 0

    @property
    def average_review(self):
        return float(self.reviews.filter(status='active').aggregate(Avg('rating'))['rating__avg'] or 0)

    @property
    def count_review(self):
        return self.reviews.filter(status='active').count()

    @property
    def sold_percentage(self):
        total = self.sold + self.available_stock
        if total > 0:
            return round((self.sold / total) * 100, 2)
        return 0

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

# =========================================================
# 08. IMAGE GALLERY MODEL
# =========================================================
class ImageGallery(BaseModel, ImageTagMixin):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='galleries/%Y/%m/%d/', default='defaults/default.jpg')

    class Meta:
        ordering = ['id']
        verbose_name_plural = '04. Image Galleries'

    def __str__(self):
        return f"{self.product.title} Image"

# =========================================================
# 09. COLOR MODEL
# =========================================================
class Color(BaseModel, ImageTagMixin):
    title = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = '05. Product Colors'

    def __str__(self):
        return f"{self.title} ({self.code})"

    @property
    def color_tag(self):
        if self.code:
            return mark_safe(
                f'<div style="width:30px; height:30px; background-color:{self.code}; border:1px solid #000;"></div>'
            )
        return ""

# =========================================================
# 10. SIZE MODEL
# =========================================================
class Size(BaseModel, ImageTagMixin):
    title = models.CharField(max_length=20, unique=True)
    code = models.CharField(max_length=10, unique=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = '06. Product Sizes'

    def __str__(self):
        return f"{self.title} ({self.code})"

# =========================================================
# 11. PRODUCT VARIANT MODEL
# =========================================================
class ProductVariant(BaseModel, ImageTagMixin):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, blank=True, null=True, on_delete=models.SET_NULL)
    size = models.ForeignKey(Size, blank=True, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='variants/%Y/%m/%d/', default='defaults/default.jpg')
    variant_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    available_stock = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = '07. Product Variants'
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'color', 'size'],
                name='unique_variant'
            )
        ]

    def clean(self):
        if not self.color and not self.size:
            raise ValidationError("Variant must have at least a color or a size.")

    def __str__(self):
        return f"{self.product.title} - {self.size or 'No Size'} - {self.color or 'No Color'}"

# =========================================================
# 12. SLIDER MODEL
# =========================================================
class Slider(BaseModel, ImageTagMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    slider_type = models.CharField(max_length=10, choices=SLIDER_TYPE_CHOICES, default='none')
    title = models.CharField(max_length=150, unique=True)
    sub_title = models.CharField(max_length=150, blank=True, null=True)
    paragraph = models.CharField(max_length=150, blank=True, null=True)
    image = models.ImageField(upload_to='sliders/%Y/%m/%d/', default='defaults/default.jpg')

    class Meta:
        ordering = ['id']
        verbose_name_plural = '08. Sliders'

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

# =========================================================
# 13. REVIEW MODEL
# =========================================================
class Review(BaseModel, ImageTagMixin):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    subject = models.CharField(max_length=50)
    comment = models.TextField(default='N/A')
    rating = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        ordering = ['id']
        verbose_name_plural = '09. Reviews'

    def __str__(self):
        return self.subject or f"Review by {self.user.username}"

# =========================================================
# 14. ACCEPTANCE PAYMENT MODEL
# =========================================================
class AcceptancePayment(BaseModel, ImageTagMixin):
    title = models.CharField(max_length=150, unique=True)
    sub_title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='acceptance_payments/%Y/%m/%d/', default='defaults/default.jpg')
    help_time = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ['id']
        verbose_name_plural = '10. Acceptance Payments'

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
