from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Listing, Message

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon_preview')
    prepopulated_fields = {'slug': ('name',)}  # Автозаполнение slug по имени
    readonly_fields = ('icon_preview',)

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" style="height: 40px;" />', obj.icon.url)
        return '—'
    icon_preview.short_description = 'Иконка'

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'created_at', 'user')
    list_filter = ('category',)
    search_fields = ('title', 'description')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'listing', 'text_preview', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('text', 'sender__username', 'recipient__username')

    def text_preview(self, obj):
        return obj.text[:50] + ('...' if len(obj.text) > 50 else '')
    text_preview.short_description = 'Текст сообщения'
