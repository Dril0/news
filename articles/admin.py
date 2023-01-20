# articles/admin.py
from django.contrib import admin
from .models import Article, Comment

class CommentInline(admin.TabularInline): 
        model = Comment
        extra = 1 #muestra cuantos fields de comentarios agrega, por defecto son 3.

class ArticleAdmin(admin.ModelAdmin): 
    inlines = [ #inlines nos muestra la relacion entre las clases de una manera visual en ela dmin.
        CommentInline, #llama a la clase CommentInLine para generar un comentario en el mismo article.
    ]

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)