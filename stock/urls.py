from django.urls import path

from . import views

app_name = 'stock'
urlpatterns = [
     path('', views.IndexView.as_view(), name='index'),
# #    path('addserver/', views.add_MailServer, name='addserver'),
# #    path('addserver/', views.EditServerView.as_view(), name='addserver'),
#     path('addserver/', views.NewServerView.as_view(), name='addserver'),
#     path('<int:usermail_pk>/edit/', views.EditServerView.as_view(), name='editserver'),
#     path('<int:reference_pk>/', views.ReferenceView.as_view(), name='detailRef'),
#     path('<int:piece_pk>/detail/', views.PiecesView.as_view(), name='detailPiece'),
     path('<int:piece_pk>/detail/', views.PieceView.as_view(), name='PieceView'),
     path('<int:piece_pk>/detail/reference/', views.PieceRef.as_view(), name='PieceRef'),
     path('<int:piece_pk>/detail/piece/', views.PieceEdit.as_view(), name='PieceEdit'),
     path('<int:piece_pk>/detail/output/', views.PieceOutput.as_view(), name='PieceOutput'),
     path('<int:piece_pk>/detail/supliers/', views.PieceSuplier.as_view(), name='PieceSuplier'),
     path('<int:piece_pk>/use/', views.PieceUse.as_view(), name='PieceUse'),
#     path('<int:usermail_pk>/checkspam/', views.CheckSpam.as_view(), name='checkspam'),
#     path('<int:usermail_pk>/unsubscribe/', views.Unsubscribe.as_view(), name='unsubscribe'),
]


from sitetree.sitetreeapp import register_dynamic_trees, compose_dynamic_tree
from sitetree.utils import tree, item
  
  
register_dynamic_trees(
  
    # or even define a tree right at the process of registration.
    compose_dynamic_tree((
        tree("maintree", title='L14SL3', items=(
            item('Home', 'stock:index', url_as_pattern=True, children=(
                item('Add Server', 'stock:addserver'),
                item('Piece Detail', 'stock:PieceView piece.pk', url_as_pattern=True, in_menu=False, children=(
                    item('Edit Reference', 'stock:PieceRef piece.pk', url_as_pattern=True),
                    item('Edit Piece', 'stock:PieceEdit piece.pk', url_as_pattern=True),
                    item('Edit Output Stock', 'stock:PieceOutput piece.pk', url_as_pattern=True),
                    item('Edit Supliers', 'stock:PieceSuplier piece.pk', url_as_pattern=True),
                    item('Use Piece', 'stock:PieceUse piece.pk', url_as_pattern=True),
                )),
            )),
        )),
    )),
  
    # Line below tells sitetree to drop and recreate cache, so that all newly registered
    # dynamic trees are rendered immediately.
    reset_cache=True
)
"""
from django.contrib.auth.models import User
user = User.objects.create_superuser('admin', '', 'admin')
"""