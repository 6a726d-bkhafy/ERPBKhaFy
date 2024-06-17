from django.urls import path, include

urlpatterns = [
    path('', include('login.urls')),
    path('inicio/', include('index.urls')),
    path('cfg/', include('cfg.urls')),
    path('parceiros/', include('parceiros.urls')),
    path('estoque/', include('estoque.urls')),
    path('financeiro/', include('financeiro.urls')),
    path('compras/', include('compras.urls')),
]
