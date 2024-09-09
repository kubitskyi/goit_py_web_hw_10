from django.contrib import admin
from app_quotes.models import Author, Quote, Tag

# Register your models here.
admin.site.register(Author)
admin.site.register(Quote)
admin.site.register(Tag)