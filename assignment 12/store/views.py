from django.shortcuts import render, get_object_or_404
from django.views import generic
from store.models import Category, Brand, Product
# Create your views here.
class HomeView(generic.View):
    def get(self, request):
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
        """
        context = {
        'borkha': Product.objects.filter(category__title__icontains='borkha'),
        }
        return render(request, "store/home.html", context)

class SingleProductView(generic.View):
    def get(self, request, slug, id):
        context = {
            'product':get_object_or_404(Product, slug=slug, id=id),
        }
        return render(request, "store/single-product.html", context)
    
class CategoryProductView(generic.View):
    def get(self, request, id):

        context = {
            'category': Product.objects.filter(category__id=id),
        }
        return render(request, "store/category-product.html", context)