from django.contrib import admin
from .models import (
    Category, Brand, Product, ProductVariant, ImageGallery,
    Color, Size, Slider, Review, AcceptancePayment
)

# =========================================================
# IMAGE TAG ADMIN MIXIN
# =========================================================
class ImageTagAdminMixin:
    readonly_fields = ('image_tag',)

# =========================================================
# CATEGORY ADMIN
# =========================================================
@admin.register(Category)
class CategoryAdmin(ImageTagAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'title', 'parent', 'status', 'is_featured', 'created_date', 'updated_date', 'image_tag', 'keyword', 'description')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', 'keyword', 'description')
    list_filter = ('status', 'is_featured')

# =========================================================
# BRAND ADMIN
# =========================================================
@admin.register(Brand)
class BrandAdmin(ImageTagAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'is_featured', 'created_date', 'updated_date', 'image_tag', 'keyword', 'description')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', 'keyword', 'description')
    list_filter = ('status', 'is_featured')

# =========================================================
# IMAGE GALLERY INLINE
# =========================================================
class ImageGalleryInline(ImageTagAdminMixin, admin.TabularInline):
    model = ImageGallery
    extra = 1
    fields = ('id', 'image', 'status', 'created_date', 'updated_date', 'image_tag')
    readonly_fields = ('image_tag',)

# =========================================================
# PRODUCT VARIANT INLINE
# =========================================================
class ProductVariantInline(ImageTagAdminMixin, admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('id', 'color', 'size', 'variant_price', 'available_stock', 'status', 'created_date', 'updated_date', 'image', 'image_tag')
    readonly_fields = ('image_tag',)

# =========================================================
# REVIEW INLINE
# =========================================================
class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    readonly_fields = ('id','user', 'subject', 'comment', 'rating', 'status', 'created_date', 'updated_date')
    can_delete = False
    fields = ('id','user', 'subject', 'comment', 'rating', 'status', 'created_date', 'updated_date')

# =========================================================
# PRODUCT ADMIN
# =========================================================
@admin.register(Product)
class ProductAdmin(ImageTagAdminMixin, admin.ModelAdmin):
    list_display = ('id','title', 'brand', 'category', 'old_price', 'sale_price', 'discount_percent', 'available_stock', 'sold', 'status', 'is_featured', 'deadline', 'is_deadline', 'created_date', 'updated_date', 'image_tag')
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('status', 'is_featured', 'brand', 'category')
    search_fields = ('title', 'keyword', 'description', 'tag', 'prev_des', 'add_des', 'short_des', 'long_des')
    inlines = [ProductVariantInline, ImageGalleryInline, ReviewInline]

# =========================================================
# COLOR ADMIN
# =========================================================
@admin.register(Color)
class ColorAdmin(ImageTagAdminMixin, admin.ModelAdmin):
    list_display = ('id','title', 'code', 'status', 'created_date', 'updated_date', 'color_tag')
    readonly_fields = ('color_tag',)
    search_fields = ('title', 'code')
    list_filter = ('status',)

# =========================================================
# SIZE ADMIN
# =========================================================
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'code', 'status', 'created_date', 'updated_date')
    search_fields = ('title', 'code')
    list_filter = ('status',)

# =========================================================
# SLIDER ADMIN
# =========================================================
@admin.register(Slider)
class SliderAdmin(ImageTagAdminMixin, admin.ModelAdmin):
    list_display = ('id','title', 'slider_type', 'status', 'is_featured', 'created_date', 'updated_date', 'image_tag', 'product', 'sub_title', 'paragraph')
    readonly_fields = ('image_tag',)
    list_filter = ('slider_type', 'status')
    search_fields = ('title', 'sub_title', 'paragraph')

# =========================================================
# REVIEW ADMIN
# =========================================================
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id','product', 'user', 'subject', 'comment', 'rating', 'status', 'created_date', 'updated_date')
    list_filter = ('status', 'rating')
    search_fields = ('product__title', 'user__username', 'subject', 'comment')

# =========================================================
# ACCEPTANCE PAYMENT ADMIN
# =========================================================
@admin.register(AcceptancePayment)
class AcceptancePaymentAdmin(ImageTagAdminMixin, admin.ModelAdmin):
    list_display = ('id','title', 'sub_title', 'status', 'is_featured', 'created_date', 'updated_date', 'image_tag', 'help_time')
    readonly_fields = ('image_tag',)
    list_filter = ('status', 'is_featured')
    search_fields = ('title', 'sub_title')
