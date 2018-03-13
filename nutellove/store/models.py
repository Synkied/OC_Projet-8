from django.db import models

# Create your models here.

# coding: utf8


class Brand(models.Model):
    name = models.CharField(unique=True, max_length=500)


class Category(models.Model):
    name = models.CharField(unique=True, max_length=500)


class Store(models.Model):
    name = models.CharField(unique=True, max_length=500)


class Product(models.Model):
    code = models.BigIntegerField()
    url = models.URLField(null=False, unique=True)
    name = models.CharField(max_length=500)
    nutri_grade = models.CharField(null=True, max_length=1)
    cat = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )
    energy = models.IntegerField(null=True)
    fat = models.FloatField(null=True)
    carbs = models.FloatField(null=True)
    sugars = models.FloatField(null=True)
    fibers = models.FloatField(null=True)
    proteins = models.FloatField(null=True)
    salt = models.FloatField(null=True)
    last_modified_t = models.DateTimeField(null=False)


class Favorite(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    substitute = models.ForeignKey(
        Product,
        related_name='products_substitute_set',
        on_delete=models.CASCADE,
    )


# many to many table
class Productbrand(models.Model):
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )


# many to many table
class Productstore(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
    )
