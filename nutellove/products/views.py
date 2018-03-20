from django.http import HttpResponse
from django.shortcuts import render
from .models import Brand, Category, Product, Favorite

# Create your views here.


def listing(request):
    products = Product.objects.filter()
    formatted_products = ["<li>{}</li>".format(product.name) for product in products]
    products = "<ul>{}</ul>".format("\n".join(formatted_products))
    context = {
        'products': products,
    }
    return render(request, 'products/list.html', context)


def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    category = Category.objects.get(pk=product.cat.id)
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
    brand = Brand.objects.get(pk=brand_id)

    context = {
        'brand': brand
    }

    return render(request, 'products/brand_details.html', context)


def search(request):
    query = request.GET.get('query')
    if not query:
        products = Product.objects.filter()[:12]  # # TODO: make a random choice
        title = "Suggestion de produits"

    else:
        # title contains the query and query is not sensitive to case.
        products = Product.objects.filter(name__icontains=query)
        title = "Résultats pour la requête {}".format(query)

    # if not products.exists():
    #     products = Product.objects.filter(category__name__icontains=query)
    #     title = "Résultats pour la requête {}".format(query)

    context = {
        'products': products,
        'title': title
    }

    return render(request, 'products/search.html', context)
