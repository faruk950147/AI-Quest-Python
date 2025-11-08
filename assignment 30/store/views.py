from django.shortcuts import render, get_object_or_404
from django.views import generic
from store.models import Category, Brand, Product, Slider


# Create your views here.
class HomeView(generic.View):
    """
    The 'category' field of the Product model is a ForeignKey to the Category model.
    This code filters the Category table's 'title' field using the value 'borkha':

    - `icontains`: case-insensitive substring matching.  
    Example: 'Borkha', 'borkha', 'BORKHA' all will match.

    - `contains`: case-sensitive substring matching.  
    Example: only 'borkha' will match; 'Borkha' or 'BORKHA' will not.

    - `iexact`: case-insensitive exact match.  
    Example: 'Borkha', 'borkha', 'BORKHA' will match, but 'borkhas' or 'borkha123' will not.

    Using these filters, you can select and display all products belonging to the 'borkha' category.
    gents_pants = Product.objects.filter(category__title__in=['GENT_PANTS'])

    """
    def get(self, request):
        sliders = Slider.objects.filter(status='ACTIVE')
        gents_pants = Product.objects.filter(category__title__contains='GENT_PANTS', status='ACTIVE')
        borkhas = Product.objects.filter(category__title__contains='BORKHA', status='ACTIVE')
        baby_fashions = Product.objects.filter(category__title__contains='BABY_FASHION', status='ACTIVE')

        categories = Category.objects.filter(status='ACTIVE')

        context = {
            'sliders': sliders, 
            'gents_pants': gents_pants, 
            'borkhas': borkhas, 
            'baby_fashions': baby_fashions,
            'categories': categories,
        }
        return render(request, "store/home.html", context)

class SingleProductView(generic.View):
    def get(self, request, slug, id):
        product = get_object_or_404(Product, slug=slug, id=id)
        context = {
            'product': product,
        }
        return render(request, "store/single-product.html", context)
    


class CategoryProductView(generic.View):
    def get(self, request, slug, id):
        category = get_object_or_404(Category, slug=slug, id=id)
        products = Product.objects.filter(category=category, status='ACTIVE')

        # Brand filter only
        selected_brands = request.GET.getlist('brand')
        if selected_brands:
            products = products.filter(brand__id__in=selected_brands).distinct()

        context = {
            'category': category,
            'products': products.order_by('-id').distinct(),
            'brands': Brand.objects.all(),
            'selected_brands': list(map(int, selected_brands)),
        }
        return render(request, "store/category-product.html", context)


    
class BrandProductView(generic.View):
    def get(self, request, slug, id):
        brand = get_object_or_404(Brand, slug=slug, id=id)
        brand_products = Product.objects.filter(brand=brand, status='ACTIVE')
        # brand_products = Product.objects.filter(brand__slug=slug, brand__id=id, status='ACTIVE')
        context = {
            'brand_products': brand_products,
        }
        return render(request, "store/brand-product.html", context)