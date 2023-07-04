from django.contrib import admin

from .models import Pessoa
# Register your models here.


class ListandoPessoas(admin.ModelAdmin):
    list_display = [
        'id',
        'nome',
        'email',
    ]
    list_display_links = [
        'id',
        'nome',
    ]
    list_per_page = 10
    ordering = [
        'id',
    ]
    list_editable = ['email']
    
    
admin.site.register(Pessoa, ListandoPessoas)
