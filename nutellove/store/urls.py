from django.urls import path

from . import views  # import views so we can use them in urls.

urlpatterns = [
    path('', views.listing),
    path('<int:album_id>', views.detail),
    path('search/', views.search),
]
