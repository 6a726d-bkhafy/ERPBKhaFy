from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('usuarios', SCListUser.as_view(), name = 'sc_list_user'),
    path('usuarios/new-password', new_password, name = 'new_password'),
    path('usuarios/new-user', new_user, name = 'new_user'),
    path('usuarios/edit-user', edit_user, name = 'edit_user'),
    path('usuarios/acessos-user', acessos_user, name = 'acessos_user'),
]

urlpatterns += [
    path('categorias', SCListCategoria.as_view(), name = 'sc_list_categoria'),
    path('categorias/new-categoria', new_categoria, name = 'new_categoria'),
    path('categorias/edit-categoria', edit_categoria, name = 'edit_categoria'),
]

urlpatterns += [
    path('custos', SCListCusto.as_view(), name = 'sc_list_custo'),
    path('custos/new-custo', new_custo, name = 'new_custo'),
    path('custos/edit-custo', edit_custo, name = 'edit_custo'),
]

urlpatterns += [
    path('juros', SCListJuro.as_view(), name = 'sc_list_juro'),
    path('juros/new-juro', new_juro, name = 'new_juro'),
    path('juros/edit-juro', edit_juro, name = 'edit_juro'),
]

urlpatterns += [
    path('contas', SCListConta.as_view(), name = 'sc_list_conta'),
    path('contas/new-conta', new_conta, name = 'new_conta'),
    path('contas/edit-conta', edit_conta, name = 'edit_conta'),
]

urlpatterns += [
    path('tipopg', SCListTipoPG.as_view(), name = 'sc_list_tipopg'),
    path('tipopg/new-tipopg', new_tipopg, name = 'new_tipopg'),
    path('tipopg/edit-tipopg', edit_tipopg, name = 'edit_tipopg'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)