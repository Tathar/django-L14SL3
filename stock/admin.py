from django.contrib import admin

from .models import Reference, OutputStock, Suplier, Piece



class ReferenceAdmin(admin.TabularInline):
    model = Reference
    
class Reference2Admin(admin.ModelAdmin):
    model = Reference
    
class OutputStockAdmin(admin.TabularInline):
    model = OutputStock
    
class OutputStock2Admin(admin.ModelAdmin):
    model = OutputStock
     
class SuplierAdmin(admin.TabularInline):
    model = Suplier
    
class Suplier2Admin(admin.ModelAdmin):
    model = Suplier

class PieceAdmin(admin.ModelAdmin):
    model = Piece
    inlines = [
        ReferenceAdmin,
        OutputStockAdmin,
        SuplierAdmin,
    ]

admin.site.register(Piece, PieceAdmin)
admin.site.register(Reference, Reference2Admin)
admin.site.register(OutputStock, OutputStock2Admin)
admin.site.register(Suplier, Suplier2Admin)
