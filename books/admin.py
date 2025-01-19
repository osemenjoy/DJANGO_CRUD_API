from django.contrib import admin
from .models import *
from django.contrib import admin


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    model = Book
    list_display = ('title', 'author', 'isbn', 'publication_date', 'availability')
    list_filter = ('title', 'author', 'isbn', 'publication_date', 'availability')
    search_fields = ('title', 'author', 'isbn') 
    ordering = ('-publication_date',)
    list_per_page = 20

