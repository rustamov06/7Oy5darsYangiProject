from django.db import models
from django.db.models import PROTECT
from django.contrib.auth.models import User



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to="category/image/", null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if not self.parent:
            return self.name
        return f"{self.parent.name}: {self.name}"


VOLUMES = {
    "kg":"Kilogram",
    "l":"Litr",
    "ta":"Dona"
}


class Product(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(default=0)
    quantity = models.IntegerField(default=50)
    volume = models.CharField(max_length=4, choices=VOLUMES)
    category = models.ForeignKey(Category, on_delete=PROTECT)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(upload_to="product/image/")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.product.name

class Comment(models.Model):
    text = models.TextField(verbose_name="Dars haqida fikringizni qoldiring")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=5)


    def __str__(self):
        return f"{self.user.name}"