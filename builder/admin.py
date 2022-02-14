from django.contrib import admin
from .models import todo


@admin.register(todo)
class todoAdmin(admin.ModelAdmin):
    
    readonly_fields =[ 'created', 'updated']
    list_display = ['user', 'note', "status","created", "updated"]
    search_fields = ['note']
    list_editable = ['note', 'status']
    
