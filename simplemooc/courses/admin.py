from django.contrib import admin
from .models import Course, Enrollment, Announcement, Comment, Lesson, Material


class CourseAdmin(admin.ModelAdmin):
    # O que mostrar no admin?
    list_display = ["name", "slug", "start_date", "created_at", "updated_at"]
    # Criar campo de busca paseado nos modelos especificados
    search_fields = ["name", "slug", "description"]
    # Preencher o slug automaticamente
    prepopulated_fields = {"slug": ("name",)}


class MaterialInlineAdmin(admin.TabularInline):
    # TabularInline -> Campos de material ordenados por coluna
    # StackedInline -> Campos de material ordenados por linha
    model = Material


class LessonAdmin(admin.ModelAdmin):
    # O que mostrar no admin?
    list_display = ["name", "number", "course", "release_date"]
    # Criar campo de busca paseado nos modelos especificados
    search_fields = ["name", "description"]
    # Criar um filtro por data
    list_filter = ["created_at"]
    # Cadastrar os materias JUNTO com a aula (inline vertical[coluna] ou horizontal[linha])
    inlines = [MaterialInlineAdmin]


# Register your models here.
admin.site.register(Course, CourseAdmin)
admin.site.register([Enrollment, Announcement, Comment, Material])
admin.site.register(Lesson, LessonAdmin)
