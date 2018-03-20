from django.urls import path

from . import views  # import views so we can use them in urls.

# required for django 2.0
app_name = "products"

urlpatterns = [
    path('', views.listing),
    path('<int:product_id>', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
]
