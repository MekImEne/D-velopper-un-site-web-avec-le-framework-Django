from django.conf.urls import url
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'blog'

urlpatterns= [
    url(r'^$', views.home, name='home'),
    path('date', views.date_actuelle),
    path('addition/<int:nombre1>/<int:nombre2>/', views.addition),
    path('', views.accueil, name='accueil'),
    path('article/<int:id>-<slug:slug>$', views.lire, name='lire'),
    url('contact/', views.contact, name='contact'),
    url('contact2/', views.nouveau_contact, name='contact2'),
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]