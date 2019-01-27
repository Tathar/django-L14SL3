from django.contrib import admin

from .models import Reference, OutputStock, Article, Suplier


class OutputStockAdmin(admin.TabularInline):
    model = OutputStock
    
class OutputStock2Admin(admin.ModelAdmin):
    model = OutputStock
     
class SuplierAdmin(admin.TabularInline):
    model = Suplier
    
class Suplier2Admin(admin.ModelAdmin):
    model = Suplier

class ArticleAdmin(admin.TabularInline):
    model = Article
    inlines = [
        SuplierAdmin,
    ]
    
class Article2Admin(admin.ModelAdmin):
    model = Article

class ReferenceAdmin(admin.ModelAdmin):
    model = Reference
    inlines = [
        OutputStockAdmin,
        ArticleAdmin,
    ]

admin.site.register(Reference, ReferenceAdmin)
admin.site.register(OutputStock, OutputStock2Admin)
admin.site.register(Suplier, Suplier2Admin)
admin.site.register(Article, Article2Admin)
