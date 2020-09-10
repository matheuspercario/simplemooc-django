from django.contrib import admin

from .models import Topic, Reply


# Register your models here.


class TopicAdmin(admin.ModelAdmin):

    list_display = ['title', 'author', 'created', 'modified']
    search_fields = ['title', 'author__email', 'body']
    # Preencher o slug automaticamente
    prepopulated_fields = {"slug": ("title",)}


class ReplyAdmin(admin.ModelAdmin):

    list_display = ['topic', 'author', 'created', 'modified']
    search_fields = ['topic__title', 'author__email', 'reply']


admin.site.register(Topic, TopicAdmin)
admin.site.register(Reply, ReplyAdmin)

# admin.site.register([Topic, Reply])
