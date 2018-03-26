import json

from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
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

    # Get the index of the current page
    index = products.number - 1  # edited to something easier without index
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(products.paginator.page_range)
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - 10 if index >= 10 else 0
    end_index = index + 10 if index <= max_index - 10 else max_index
    # Get our new page range.
    # In the latest versions of Django page_range returns an iterator.
    # Thus pass it to list, to make our slice possible again.
    page_range = list(products.paginator.page_range)[start_index:end_index]

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

    def get(self, request):
        """
        Used to handle queries from user and perform a search
        """
        query = request.GET.get('query')
        # page = request.GET.get('page')

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

                # comment to display pagination
                # products = better_products[:6]

                # uncomment to display pagination
                products = view_pagination(request, 6, better_products)

                page_range = page_indexing(products, 10)

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

        context = {
            'chosen_product': chosen_product,
            'products': products,
            'title': title,
            'paginate': True,
            'query': query,
            'page_range': page_range,
        }

        return render(request, 'products/search.html', context)


class FavoriteView(View):
    # pass the model in path args in urls.py
    model = None

    def post(self, request, pk):
        # We need a user
        user = auth.get_user(request)
        # Trying to get a bookmark from the table, or create a new one
        favorite, created = self.model.objects.get_or_create(user=user, obj_id=pk)
        # If no new bookmark has been created,
        # Then we believe that the request was to delete the bookmark
        if not created:
            favorite.delete()

        return HttpResponse(
            json.dumps({
                "result": created,
                "count": self.model.objects.filter(obj_id=pk).count()
            }),
            content_type="application/json"
        )
