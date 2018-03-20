# from django.http import HttpResponse
# from django.shortcuts import render
# from .models import Brand, Category, Product, Favorite


# def search(request):
#     query = request.GET.get('query')
#     if not query:
#         products = Product.objects.all()

#     else:
#         # title contains the query and query is not sensitive to case.
#         products = Product.objects.filter(name__icontains=query)

#     if not products.exists():
#         message = "Misère de misère, nous n'avons trouvé aucun résultat !"

#     else:
#         products = ["<li>{}</li>".format(product.name) for product in products]
#         message = """
#             Nous avons trouvé les produits correspondant à votre requête ! Les voici :
#             <ul>{}</ul>
#         """.format("".join(products))

#     return HttpResponse(message)
