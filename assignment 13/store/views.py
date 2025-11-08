from django.shortcuts import render, get_object_or_404
from django.views import generic
from store.models import Category, Brand, Product, Slider
from django.db.models import Prefetch

# Create your views here.
class HomeView(generic.View):
    """
    # 1. Case-insensitive substring search 
    # Example: "Pant", "pant", "PANT" — all will match
    products = Product.objects.filter(category__title__icontains='pant')

    # 2. Case-sensitive substring search
    # Example: only "pant" will match; "PANT" or "Pant" will not
    products = Product.objects.filter(category__title__contains='pant')

    # 3. Case-insensitive exact match 
    # Example: "pant", "PANT", "Pant" — all will match, 
    # but "pants" or "pant123" will not
    products = Product.objects.filter(category__title__iexact='pant')

    # 4. Multiple match using 'in' lookup
    # This returns all products whose category title is either 
    # 'pant', 'shirt', or 'howdy'
    products = Product.objects.filter(category__title__in=['pant', 'shirt', 'howdy'])        
    shirts = Product.objects.filter(category__title__in="SHIRT", status='ACTIVE').select_related('category')
    """
    def get(self, request):
        
        context = {
        }
        return render(request, "store/home.html", context)

class SingleProductView(generic.View):
    def get(self, request, slug, id):
        product = get_object_or_404(Product, slug=slug, id=id),
        context = {
            'product': product,
        }
        return render(request, "store/single-product.html", context)
    
class CategoryProductView(generic.View):
    def get(self, request, slug, id):
        context = {
        }
        return render(request, "store/category-product.html", context)