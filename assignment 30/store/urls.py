from django.urls import path
from store.views import (
    HomeView, SingleProductView, CategoryProductView, SearchProductView, GettingFilteredProductsView
)
urlpatterns = [
    # Define your URL patterns here
    path('', HomeView.as_view(), name='home'),
    path('single-product/<str:slug>/<int:id>/', SingleProductView.as_view(), name='single-product'),
    path('category-product/<str:slug>/<int:id>/', CategoryProductView.as_view(), name='category-product'),
    path('getting-filtered-products/<str:slug>/<int:id>/', GettingFilteredProductsView.as_view(), name='getting-filtered-products'),
    path('search-product/', SearchProductView.as_view(), name='search-product'),
]




    
