from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from .form import CommentFrom
from .models import Product, Category, ProductImage, Comment







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


class ProductDetailView(View):
    """Mahsulot sahifasi va kommentlarni boshqarish"""

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)  # Slug orqali olish
        comments = Comment.objects.filter(product=product)
        form = CommentFrom()
        context = {"product": product, "comments": comments, "form": form}
        return render(request, "product_detail.html", context)

    @method_decorator(login_required)
    def post(self, request, slug):
        """Faqat tizimga kirgan foydalanuvchilar izoh qoldira, o‘chira va tahrirlaya oladi"""
        product = get_object_or_404(Product, slug=slug)
        action = request.POST.get("action")

        if action == "create":
            form = CommentFrom(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.product = product
                comment.user = request.user
                comment.save()

        elif action == "update":
            comment_id = request.POST.get("comment_id")
            comment = get_object_or_404(Comment, id=comment_id, product=product)
            if request.user == comment.user:
                comment.text = request.POST.get("text")
                comment.save()

        elif action == "delete":
            comment_id = request.POST.get("comment_id")
            comment = get_object_or_404(Comment, id=comment_id, product=product)
            if request.user == comment.user:
                comment.delete()

        return redirect("product_detail", slug=product.slug)