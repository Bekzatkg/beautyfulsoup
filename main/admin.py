from django.contrib import admin
from .models import *


class PostImageInline(admin.TabularInline):
    model = PostImage
    max_num = 10
    min_num = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline, ]


admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Like)
admin.site.register(Favorite)
