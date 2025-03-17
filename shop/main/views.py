from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from .form import CommentFrom
from .models import Product, Category, ProductImage, Comment
from django.db.models import Max, Min, Count, Sum, Avg
from django.core.paginator import Paginator


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
        context['product_max_discount'] = Product.objects.aggregate(Max('discount'))
        context['product_max_discount'] = Product.objects.filter(discount__gt=0, slug__isnull=False).order_by('-discount')

        context['min_price'] = Product.objects.aggregate(Min('price'))['price__min']
        context['max_price'] = Product.objects.aggregate(Max('price'))['price__max']
        return context


    def get_queryset(self):
            queryset = Product.objects.all()

            min_price = self.request.GET.get('min_price')
            max_price = self.request.GET.get('max_price')

            if min_price and max_price:
                queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

            return queryset




class ProductDetailView(View):

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)  # Slug orqali olish
        comments = Comment.objects.filter(product=product)
        form = CommentFrom()
        context = {"product": product, "comments": comments, "form": form}
        return render(request, "product_detail.html", context)

    @method_decorator(login_required)
    def post(self, request, slug):
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

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        subcategories = Category.objects.filter(parent=self.object)

        if subcategories.exists():
            products = Product.objects.filter(category__in=subcategories)
        else:
            products = Product.objects.filter(category=self.object)

        paginator = Paginator(products, 10)
        page_number = self.request.GET.get('page')
        products_page = paginator.get_page(page_number)

        context['subcategories'] = subcategories
        context['products'] = products_page

        return context


