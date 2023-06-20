from django.contrib import admin

from .models import Prato
# Register your models here.


class ListandoPratos(admin.ModelAdmin):
    list_display = [
        'id',
        'nome_prato',
        'categoria',
        'tempo_preparo',
        'rendimento',
        'publicado',
    ]
    list_display_links = [
        'id',
        'nome_prato',
    ]
    list_filter = [
        'categoria',
    ]
    list_per_page = 6
    search_fields = [
        'nome_prato',
        'categoria',
    ]
    list_editable = [
        'categoria',
        'publicado',
    ]
    ordering = [
        'id',
    ]
    




admin.site.register(Prato, ListandoPratos)
