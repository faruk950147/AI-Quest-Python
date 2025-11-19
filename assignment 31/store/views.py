from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Max, Min
from store.models import Category, Brand, Product, Slider


# Create your views here.
@method_decorator(never_cache, name='dispatch')
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
        sliders = Slider.objects.filter(status='ACTIVE')
        gents_pants = Product.objects.filter(category__title__contains='GENT PANTS', status='ACTIVE')
        borkhas = Product.objects.filter(category__title__contains='BORKHA', status='ACTIVE')
        baby_fashions = Product.objects.filter(category__title__contains='BABY FASHION', status='ACTIVE')

        context = {
            'sliders': sliders, 
            'gents_pants': gents_pants, 
            'borkhas': borkhas, 
            'baby_fashions': baby_fashions,
        }
        return render(request, "store/home.html", context)

@method_decorator(never_cache, name='dispatch')
class SingleProductView(generic.View):
    def get(self, request, slug, id):
        product = get_object_or_404(Product, slug=slug, id=id)
        context = {
            'product': product,
        }
        return render(request, "store/single-product.html", context)

@method_decorator(never_cache, name='dispatch')
class CategoryProductView(generic.View):
    def get(self, request, slug, id):
        category = get_object_or_404(Category, slug=slug, id=id)
        products = Product.objects.filter(category=category, status='ACTIVE')
        brands = Brand.objects.filter(product__category=category).distinct()

        max_price = products.aggregate(Max('sale_price'))['sale_price__max']
        min_price = products.aggregate(Min('sale_price'))['sale_price__min']

        context = {
            'category': category,
            'products': products,
            'brands': brands,
            'max_price': max_price,
            'min_price': min_price,
        }
        return render(request, 'store/category-product.html', context)

@method_decorator(never_cache, name='dispatch')
class GetFilterProductsView(generic.View):
    def post(self, request):
        id = request.POST.get('id')
        slug = request.POST.get('slug')
        category = get_object_or_404(Category, id=id, slug=slug)

        products = Product.objects.filter(category=category, status='ACTIVE')

        # Brand filter
        brand_ids = request.POST.getlist('brand[]')
        if brand_ids:
            products = products.filter(brand_id__in=brand_ids)

        # Price filter
        max_price = request.POST.get('maxPrice')
        if max_price:
            products = products.filter(sale_price__lte=max_price)

        html = render_to_string('store/product_grid.html', {'products': products})
        return JsonResponse({'html': html})
    
@method_decorator(never_cache, name='dispatch')
class SearchProductView(generic.View):
    def post(self, request):
        q = request.POST.get('q', '').strip()

        if q:
            products = Product.objects.filter(title__icontains=q)
        else:
            products = Product.objects.none()

        return render(request, 'store/search-results.html', {
            'products': products,
            'count_products': products.count(),
        })
    