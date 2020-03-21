from django.conf.urls import url
from django.urls import path
from . import views
from .models import Article
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView, ListView  # L'import a changé, attention !

app_name = 'blog'

urlpatterns= [
    url(r'^$', views.home, name='home'),
    path('date', views.date_actuelle),
    path('addition/<int:nombre1>/<int:nombre2>/', views.addition),
    path('', views.accueil, name='accueil'),
    path('article/<int:id>-<slug:slug>$', views.lire, name='lire'),
    url('contact/', views.contact, name='contact'),
    url('contact2/', views.nouveau_contact, name='contact2'),
    #static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    #url('faq', views.faq, name='faq'),
    #url(r'^faq$', views.FAQView.as_view()),   # Nous demandons la vue correspondant à la classe FAQView
    url(r'^faq', TemplateView.as_view(template_name='blog/faq.html')),

    # Nous allons réécrire l'URL de l'accueil
    #url(r'^$', ListView.as_view(model=Article,
     #                           context_object_name="derniers_articles",
       #                         template_name="blog/accueil.html")),
    url(r'^$', views.ListeArticles.as_view(), name="blog_liste"),
    url(r'^categorie/(\d+)$', views.ListeArticles.as_view(), name='blog_categorie'),

    # Et nous avons toujours nos autres pages…
    url(r'^article/(?P<id>\d+)$', views.lire),
    #url(r'^(?P<page>\d+)$', views.archives),
    #url(r'^categorie/(?P<slug>.+)$', views.voir_categorie),

    url(r'^categorie/(\w+)$', views.ListeArticles.as_view()),
    url(r'^article/(?P<pk>\d+)$', views.LireArticle.as_view(), name='blog_lire'),


]