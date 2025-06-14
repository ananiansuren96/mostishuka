from django.contrib import admin
from .models import Category, Listing

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon_preview')
    prepopulated_fields = {'slug': ('name',)}  # Автозаполнение slug по имени
    readonly_fields = ('icon_preview',)

    def icon_preview(self, obj):
        if obj.icon:
            return f'<img src="{obj.icon.url}" style="height: 40px;" />'
        return '—'
    icon_preview.allow_tags = True
    icon_preview.short_description = 'Иконка'

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'description')
