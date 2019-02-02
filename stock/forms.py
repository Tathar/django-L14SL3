from django import forms
from django.forms import inlineformset_factory
from .models import Reference, OutputStock, Suplier, Piece
from django.utils.translation import ugettext_lazy as _

# from djangoformsetjs.utils import formset_media_js


# class EditUserMail(NewUserMail):
#     password = forms.CharField(required = False, label='Mot de passe', max_length=100,widget=forms.PasswordInput())
#  
# 

class UsePiece(forms.Form):
    Date = forms.DateField(label=_("date Changed"), help_text=_("when did you change this piece?"))
    Qt = forms.IntegerField(label=_("Mouvement quantity"), help_text=_(""))
    Next_needed = forms.DateField(label=_("Next time needed"), help_text=_("when will you change this piece next time?"), required=False)


ReferencesFormView = inlineformset_factory(Piece, Reference, fields = ('PN',), extra=0, can_delete=True )
OutputStocksFormView = inlineformset_factory(Piece, OutputStock, fields = ('Date','Qt',), extra=0, can_delete=True )
SupliersFormView = inlineformset_factory(Piece, Suplier, fields = ('Manufacturer', 'Suplier', 'Ref',), extra=0, can_delete=True )

