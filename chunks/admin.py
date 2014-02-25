from django.contrib import admin
from models import Chunk


class ChunkAdmin(admin.ModelAdmin):
    list_display = ('name', 'key',)
    search_fields = ('name', 'key', 'content')
    prepopulated_fields = {'key': ('name',)}

admin.site.register(Chunk, ChunkAdmin)
