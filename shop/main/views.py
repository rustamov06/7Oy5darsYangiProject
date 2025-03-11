from django.shortcuts import render
from django.views.generic import ListView
from .models import Product, Category, ProductImage




class IndexView(ListView):
    queryset = Product.objects.all()[:10]
    template_name = "index.html"
    context_object_name = 'products'



    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = Category.objects.filter(parent=None)
        images = []
        for image in ProductImage.objects.all():
            images.append(image.image.url)
        context['images'] = images
        return context


