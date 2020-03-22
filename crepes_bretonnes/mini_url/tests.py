from django.test import TestCase
from django.urls import reverse
from .models import MiniURL
from .views import generer

def creer_url():
    mini = MiniURL(url="http://foo.bar",code=generer(6), pseudo="Maxime")
    mini.save()
    return

def test_nouveau_redirection(self):
    """ Vérifie la redirection d'un ajout d'URL """
    data = {
        'url': 'http://www.djangoproject.com',
        'pseudo': 'Jean Dupont',
    }

    reponse = self.client.post(reverse('mini_url.views.nouveau'), data)
    self.assertEqual(reponse.status_code, 302)
    self.assertRedirects(reponse, reverse('mini_url.views.liste'))

def test_nouveau_ajout(self):
    """
    Vérifie si après la redirection l'URL ajoutée est bien dans la liste
    """
    data = {
        'url': 'http://www.crepes-bretonnes.com',
        'pseudo': 'Amateur de crêpes',
    }

    reponse = self.client.post(reverse('mini_url.views.nouveau'), data, follow=True)
    self.assertEqual(reponse.status_code, 200)
    self.assertContains(reponse, data['url'])



class MiniURLTests(TestCase):
    def test_liste(self):
        """ Vérifie si une URL sauvegardée est bien affichée """

        mini = creer_url()
        reponse = self.client.get(reverse('mini_url.views.liste'))

        self.assertEqual(reponse.status_code, 200)
        self.assertContains(reponse, mini.url)
        self.assertQuerysetEqual(reponse.context['minis'], [repr(mini)])
