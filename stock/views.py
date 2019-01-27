from django.shortcuts import render
from django.views import generic

from .models import Reference, OutputStock, Article, Suplier


class IndexView(generic.ListView):
    template_name = 'stock/index.html'
#    context_object_name = 'ViewAllReference'
    http_method_names = ['get',]
    model = Reference
    extra_context = {"Object": Reference }

class ReferenceView(generic.DetailView):
    template_name = 'stock/referenceView.html'
#    context_object_name = 'ViewAllReference'
    http_method_names = ['get',]
    model = Reference
    extra_context = {}
    pk_url_kwarg = 'reference_pk'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
         
        context["OutputStocks"] = self.object.outputstock_set.all()
        context["Articles"] = []
        for article in self.object.article_set.all() :
            mydict = { "article" : article }
            mydict["supliers"] = article.suplier_set.all()           
            context["Articles"].append( mydict )
            
        return context