from django.shortcuts import render
from django.views import generic
from store.models import Category, Brand, Product
# Create your views here.
class HomeView(generic.View):
    def get(self, request):
        context = {
        """ Product model category is ForeignKey (Category model) type
        it code Category table title field 'borkha' icontains filter use
        borkha category product select and show """
        
        'borkha': Product.objects.filter(category__title__icontains='borkha')
        

        }
        return render(request, "store/home.html", context)

class SingleProductView(generic.View):
    def get(self, request):
        context = {

        }
        return render(request, "store/single-product.html", context)
    
class CategoryProductView(generic.View):
    def get(self, request, id):

        category = Product.objects.filter(category__id=id)
        print(category)

        context = {
            'category': category,
        }
        return render(request, "store/category-product.html", context)