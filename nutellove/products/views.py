from random import randint

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Brand, Category, Product, Favorite
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.translation import gettext
from django.views import View

# Create your views here.


def view_pagination(request, n_el, model_elem):
    """
    Function to use paginator in many views
    """
    paginator = Paginator(model_elem, n_el)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an int, deliver the first page.
        products = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999),
        # deliver last page of results.
        products = paginator.page(paginator.num_pages)

    return (products)


def listing(request):
    """
    List all available products on a page
    """
    products_list = Product.objects.filter()

    products = view_pagination(request, 12, products_list)
    title = gettext("Tous nos produits")

    context = {
        'products': products,
        'title': title,
        'paginate': True,
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
        'product_name': product.name,
        'brands': brands,
        'stores': stores,
        'product_id': product.id,
        'img': product.img,
        'url': product.url,
        'category': category.name,
        'nutri_grade': product.nutri_grade,
        'energy': product.energy,
        'fat': product.fat,
        'carbs': product.carbs,
        'sugars': product.sugars,
        'fibers': product.fibers,
        'proteins': product.proteins,
        'salt': product.salt,
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

    def __init__(self):
        self.chosen_product = False

    def get(self, request):
        """
        Used to handle queries from user and perform a search
        """
        query = request.GET.get('query')
        # page = request.GET.get('page')

        if not query:
            products = Product.objects.filter()[:12]  # # TODO: make a random choice
            title = gettext("Suggestion de produits")

        else:
            # title contains the query and query is not sensitive to case.
            products_list = Product.objects.filter(name__icontains=query)
            # chose a random product from the query

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

                products = view_pagination(request, 6, better_products)

            else:
                chosen_product = None
                products = products_list

            title = gettext(
                "Résultats pour la requête {}".format(
                    query.capitalize()
                )
            )

        # if not products.exists():
        #     products = Product.objects.filter(category__name__icontains=query)
        #     title = "Résultats pour la requête {}".format(query)

        context = {
            'chosen_product': chosen_product,
            'products': products,
            'title': title,
            'paginate': True,
            'query': query,
        }

        return render(request, 'products/search.html', context)
