from django.contrib import admin
from .models import  Category, Product, ProductImage, Comment
from django.utils.safestring import mark_safe


admin.site.register(ProductImage)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'get_image')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ("name",)}

    def get_image(self, category):
        if category.image:
            return mark_safe(f'<img src="{category.image.url}" width="100">')
        return 'Image not available'

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'discount', 'quantity', 'volume', 'get_image')
    list_display_links = ('name',)
    prepopulated_fields = {'slug':("name",)}
    inlines = [ProductImageInline]

    def get_image(self, product):
        image = product.images.all()
        if image:
            return mark_safe(f'<img src="{image[0].image.url}" width="100" >')
        return 'Image not available'

@admin.register(Comment)
class Commentadmin(admin.ModelAdmin):
    list_display = ('text',)
    list_display_links = ('text',)
