from django.urls import path

from . import views  # import views so we can use them in urls.

# required for django 2.0
app_name = "products"

urlpatterns = [
    # what to display for url products/
    path('', views.listing),
    # what to display for url products/<id>
    path('<int:product_id>', views.product_detail, name='product_detail'),
    # what to display for url products/search/?query=<query>
    path('search/', views.search, name='search'),
]