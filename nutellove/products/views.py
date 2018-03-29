from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from .models import Brand, Category, Product, Favorite
from .controllers import view_pagination, page_indexing
from django.utils.translation import gettext
from django.views import View

# Create your views here.


def listing(request):
    """
    List all available products on a page
    """
    products_list = Product.objects.filter()

    products = view_pagination(request, 9, products_list)
    title = gettext("Tous nos produits")

    page_range = page_indexing(products, 10)

    context = {
        'products': products,
        'title': title,
        'paginate': True,
        'page_range': page_range,
    }

    return render(request, 'products/listing.html', context)


def product_detail(request, product_id):
    """
    Used to display the details of a product
    """
    product = get_object_or_404(Product, pk=product_id)
    category = get_object_or_404(Category, pk=product.cat.id)
    brands = [brand.name for brand in product.brands.all()]
    stores = [store.name for store in product.stores.all()]

    context = {
        'product': product,
        'brands': brands,
        'stores': stores,
        'category': category.name,
    }

    return render(request, 'products/product_details.html', context)


def brand_detail(request, brand_id):
    """
    Used to give details of a brand
    """
    brand = get_object_or_404(Brand, pk=brand_id)

    context = {
        'brand': brand
    }

    return render(request, 'products/brand_details.html', context)


class Search(View):

    template_name = 'products/search.html'

    def get(self, request):
        """
        Used to handle queries from user and perform a search
        """
        query = request.GET.get('query')

        user = auth.get_user(request)

        if not query:
            products_list = Product.objects.filter()

            products = view_pagination(request, 6, products_list)

            page_range = page_indexing(products, 10)

            title = gettext("Suggestion de produits")

            chosen_product = None
            page_range = None

        else:
            # title contains the query and query is not sensitive to case.
            products_list = Product.objects.filter(name__icontains=query)

            if len(products_list) > 0:
                chosen_product = products_list[0]

                if chosen_product.nutri_grade == "a":
                    better_products = [
                        product for product in products_list
                        if product.nutri_grade == chosen_product.nutri_grade
                    ]
                else:
                    better_products = [
                        product for product in products_list
                        if product.nutri_grade < chosen_product.nutri_grade
                    ]

                # !!!! comment to display pagination
                products = better_products[:8]
                page_range = None

                # !!!! uncomment to display pagination
                # products = view_pagination(request, 8, better_products)
                # page_range = page_indexing(products, 10)

            else:
                chosen_product = None
                page_range = None
                products = products_list

            # title = gettext(
            #     "Résultats pour la requête {}".format(
            #         query.capitalize()
            #     )
            # )

            title = ""

        # check if user is not anonymous
        if user.username != "":
            for product in products:
                if Favorite.objects.filter(substitute=product, user=user).exists():
                    product.is_favorite = True
                else:
                    product.is_favorite = False

        context = {
            'chosen_product': chosen_product,
            'products': products,
            'title': title,
            'paginate': True,
            'query': query,
            'page_range': page_range,
        }

        return render(request, self.template_name, context)


class FavoriteView(LoginRequiredMixin, View):
    # pass the model in path args in urls.py
    # e.g: FavoriteView.as_view(model=Favorite)
    model = None
    template_name = 'products/favorites.html'

    def get(self, request):

        user = auth.get_user(request)
        favorites = Favorite.objects.filter(user=user)

        context = {
            'favorites': favorites
        }

        return render(request, self.template_name, context)

    def post(self, request, product_id):

        # Get the user if connected
        user = auth.get_user(request)

        # Trying to get a favorite from the database, or create a new one
        product = Product.objects.get(pk=product_id)
        favorite, created = self.model.objects.get_or_create(substitute=product, user=user)

        # If no new bookmark has been created,
        # Then we believe that the request was to delete the bookmark
        if not created:
            favorite.delete()

        # return the same/previous page, or the index if fail
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', ''))
