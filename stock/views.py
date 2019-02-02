from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic

from .models import Reference, OutputStock, Suplier, Piece


from .forms import ReferencesFormView, OutputStocksFormView, SupliersFormView, UsePiece
from .mixin import ajaxGetMixin, ObjectFormView
from django.urls import reverse, reverse_lazy



class IndexView(generic.ListView):
    template_name = 'stock/index.html'
#    context_object_name = 'ViewAllReference'
    http_method_names = ['get',]
    model = Piece
    extra_context = {"Object": Piece }

# class PiecesView(generic.DetailView):
#     template_name = 'stock/referenceView.html'
# #    context_object_name = 'ViewAllReference'
#     http_method_names = ['get',]
#     model = Piece
#     extra_context = {}
#     pk_url_kwarg = 'piece_pk'
#     
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#          
#         context["OutputStocks"] = self.object.outputstock_set.all()
#         context["References"] = self.object.reference_set.all()
#         context["Articles"] = []
#         for article in self.object.article_set.all() :
#             mydict = { "article" : article }
#             mydict["supliers"] = article.suplier_set.all()           
#             context["Articles"].append( mydict )
#             
#        return context
    



class BasePiece(generic.UpdateView):
    template_name = 'stock/piece_view.html'
    model = Piece
    pk_url_kwarg = 'piece_pk'
    fields = ['Name', "Description", "Position", "StockQt", "Already_used", "Next_needed"]
    
    def get_context_data(self, **kwargs):
        if self.request.method == "POST" :
            kwargs["Referances"] = ReferencesFormView(self.request.POST, instance = self.object)
            kwargs["Referances"].full_clean()
            kwargs["OutputStocks"] = OutputStocksFormView(self.request.POST, instance = self.object)
            kwargs["OutputStocks"].full_clean()
            kwargs["Supliers"] = SupliersFormView(self.request.POST, instance = self.object)
            kwargs["Supliers"].full_clean()
        else :
            kwargs["Referances"] = ReferencesFormView(instance = self.object)
            kwargs["OutputStocks"] = OutputStocksFormView(instance = self.object)
            kwargs["Supliers"] = SupliersFormView(instance = self.object)
        
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        
        if form.has_changed():
            form.save()
            
        context = self.get_context_data()
        Referances = context['Referances']
        OutputStocks = context['OutputStocks']
        Supliers = context['Supliers']
        
        if Referances.has_changed():
            if Referances.is_valid() :
                Referances.save()
            else :
                return self.form_invalid(form)
            
        if OutputStocks.has_changed():
            if OutputStocks.is_valid() :
                OutputStocks.save()
            else :
                return self.form_invalid(form)
            
        if Supliers.has_changed() :
            if Supliers.is_valid() :
                Supliers.save()
            else :
                return self.form_invalid(form)
        
        
        return HttpResponseRedirect(reverse('stock:PieceView',args=[self.object.pk]))

    
class PieceView(BasePiece):
    template_name = 'stock/piece_view.html'
    
class PieceRef(BasePiece):
    template_name = 'stock/piece_edit_ref.html'
    
class PieceEdit(BasePiece):
    template_name = 'stock/piece_edit_piece.html'
    
class PieceOutput(BasePiece):
    template_name = 'stock/piece_edit_output.html'
    
class PieceSuplier(BasePiece):
    template_name = 'stock/piece_edit_suplier.html'



class PieceUse(generic.UpdateView):
    template_name = 'stock/piece_use.html'
    model = Piece
    pk_url_kwarg = 'piece_pk'
    form_class=UsePiece
    initial = {}
    
    def form_valid(self, form):
        
        fields = form.cleaned_data
        
        output = self.object.outputstock_set.create(Date=fields['Date'] ,Qt=fields["Qt"])
        output.save()
        
        if self.object.Next_needed != fields["Next_needed"] :
            self.object.Next_needed = fields["Next_needed"]
            self.object.save()
        
        return HttpResponseRedirect(reverse('stock:PieceView',args=[self.object.pk]))
        
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
            
        return kwargs
    
