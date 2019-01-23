from django.db import models
from django.utils.translation import ugettext_lazy as _

import datetime

# Create your models here.
class Article(models.Model):
    HK_pn = models.CharField(_("HK Part number"), help_text=_("Part number of this HK piece"), max_length=32,blank=False, unique = True, db_index = True)
    HK_name = models.CharField(_("HK Name"), help_text=_("Name of this HK piece"), max_length=64,blank=False, db_index = True)
    HK_description = models.TextField(_("HK Description"), blank = True, help_text=_("description of this HK piece"))
    Position = models.CharField(_("Position"), help_text=_("position in stok of this piece"), max_length=254)
    Qt = models.IntegerField(_("Quantity"), help_text=_(""))
    Suplier = models.CharField(_("Supplier"), help_text=_("Suplier of this piece"), blank = True, max_length=64)
    Producteur = models.CharField(_("Producer"), help_text=_("Producer of this piece"), blank = True, max_length=64)
    Prod_pn = models.CharField(_("Producer part number"), help_text=_("part number of prudcter piece"), blank = True, max_length=32)
    Already_used = models.DateField(_("Alredy used date"), help_text=_("when did you use this piece?"), blank = True)
    Last_changed = models.DateField(_("Last date Changed"), help_text=_("when did you change this piece for the last time?"), blank = True)
    Next_needed = models.DateField(_("Next time needed"), help_text=_("when will you change this piece next time?"), blank = True)

    def __str__(self):
        return self.HK_name +"("+ self.HK_pn +")"