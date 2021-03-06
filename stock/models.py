from django.db import models
from django.utils.translation import ugettext_lazy as _

import datetime
from django.template.defaultfilters import default

from django.dispatch import receiver
from symbol import except_clause

# Create your models here.
class Piece(models.Model):
    """Définit une référence issue du "Part List" """
    Name = models.CharField(_("HK Name"), help_text=_("Name of this HK piece"), max_length=64, blank=False, db_index = True)
    Description = models.TextField(_("HK Description"), help_text=_("description of this HK piece"), blank = True)
    Position = models.CharField(_("Stock position"), help_text=_("position in stok of this piece"), max_length=254, blank = True)
    StockQt = models.IntegerField(_("Stock quantity"), default = 0)
    Already_used = models.IntegerField(_("Already used"), help_text=_("number of times this reference was used"), default = 0, blank = True)
#    Suplier = models.CharField(_("Supplier"), help_text=_("Suplier of this piece"), blank = True, max_length=64)
#    Producteur = models.CharField(_("Producer"), help_text=_("Producer of this piece"), blank = True, max_length=64)
#    Prod_pn = models.CharField(_("Producer part number"), help_text=_("part number of prudcter piece"), blank = True, max_length=32)
#    Already_used = models.DateField(_("Alredy used date"), help_text=_("when did you use this piece?"), blank = True)
#    Last_changed = models.DateField(_("Last date Changed"), help_text=_("when did you change this piece for the last time?"), blank = True)
    Next_needed = models.DateField(_("Next time needed"), help_text=_("when will you change this piece next time?"), blank = True, null=True)
    
    def __str__(self):
        return self.Name +" ( "+ str(self.reference_set.first().PN) +" )"
    
class Reference(models.Model):
    """Définit une référence issue du "Part List" """
    PN = models.CharField(_("HK Part number"), help_text=_("Part number of this HK piece"), max_length=32,blank=False, unique = True, db_index = True)
    Piece = models.ForeignKey(Piece, on_delete=models.CASCADE)


class OutputStock(models.Model):
    """date de sortie de stock pour cette référence"""
    Piece = models.ForeignKey(Piece, on_delete=models.CASCADE)
    Date = models.DateField(_("date Changed"), help_text=_("when did you change this piece?"), default=datetime.date.today)
    Qt = models.IntegerField(_("Mouvement quantity"), help_text=_(""), default = 1)
    
    @classmethod
    def pre_save(cls, sender, **kwargs):
        """a l'ajout d'un "OutputStock" (sortie de stock) """
        obj = kwargs["instance"]
        
        try :
            old = sender.objects.get(pk=obj.pk)
            obj.Piece.StockQt += old.Qt
            obj.Piece.Already_used -= old.Qt
        except :
            pass
        
        obj.Piece.StockQt -= obj.Qt
        obj.Piece.Already_used += obj.Qt
        obj.Piece.save()
            
#     @classmethod
#     def post_save(cls, sender, **kwargs):
#         """a l'ajout d'un "OutputStock" (sortie de stock) """
#         if kwargs["created"] :
#             print ('post save')
#             obj = kwargs["instance"]
#             obj.Piece.StockQt -= obj.Qt
#             obj.Piece.Already_used += obj.Qt
#             obj.Piece.save()
            
    @classmethod
    def pre_delete(cls, sender, **kwargs):
        """a la supression d'un "OutputStock" (retour en stock) """
        print ('pre delete')
        obj = kwargs["instance"]
        obj.Piece.StockQt += obj.Qt
        obj.Piece.Already_used -= obj.Qt
        obj.Piece.save()

    def __str__(self):
        return self.Piece.Name +" ( "+ str(self.Date) +" )"
    
models.signals.pre_save.connect(OutputStock.pre_save, sender=OutputStock)
models.signals.pre_delete.connect(OutputStock.pre_delete, sender=OutputStock)
    
class Suplier(models.Model):
    Piece = models.ForeignKey(Piece, on_delete=models.CASCADE)
    Manufacturer = models.CharField(_("Manufacturer"), help_text=_("Manufacturer of this piece"), max_length=64)
    Suplier = models.CharField(_("Sulier Name"), help_text=_("Name of the supplier"), blank = True, max_length=64)
    Ref = models.CharField(_("supplier reference"), help_text=_("part reference at the supplier"), blank = True, max_length=32)
    
