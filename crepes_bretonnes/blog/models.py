from django.db import models
from django.utils import timezone
#from django.contrib import admin
#from .views import renommage

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

class Categorie(models.Model):
    nom = models.CharField(max_length=30)

    def __str__(self):
        return self.nom


class Article(models.Model):
    titre = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    auteur = models.CharField(max_length=42)
    contenu = models.TextField(null=True)
    date = models.DateTimeField(default=timezone.now,
                                verbose_name="Date de parution")
    categorie = models.ForeignKey('Categorie', on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.titre


class Moteur(models.Model):
    nom = models.CharField(max_length=25)

    def __str__(self):
        return self.nom


class Voiture(models.Model):
    nom = models.CharField(max_length=25)
    moteur = models.OneToOneField(Moteur, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom


class Produit(models.Model):
    nom = models.CharField(max_length=30)

    def __str__(self):
        return self.nom


class Vendeur(models.Model):
    nom = models.CharField(max_length=30)
    produits = models.ManyToManyField(Produit, through='Offre',
                                      related_name='+')
    produits_sans_prix = models.ManyToManyField(Produit, related_name="vendeurs")

    def __str__(self):
        return self.nom


class Offre(models.Model):
    prix = models.IntegerField()
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    vendeur = models.ForeignKey(Vendeur, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} vendu par {1}".format(self.produit, self.vendeur)


class Contact(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.TextField()
    photo = models.ImageField(upload_to="photos/")

    def __str__(self):
        return self.nom


#class Document(models.Model):
   # nom = models.CharField(max_length=100)
   # doc = models.FileField(upload_to=renommage, verbose_name="Document")



# Les modèles parents abstraits

class Document(models.Model):
    titre = models.CharField(max_length=255)
    date_ajout = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Date d'ajout du document")
    auteur = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True


class Article2(Document):
    contenu = models.TextField()


class Image(Document):
    image = models.ImageField(upload_to="images")



# Les modèles parents classiques
class Lieu(models.Model):
    nom = models.CharField(max_length=50)
    adresse = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Restaurant(Lieu):
    menu = models.TextField()



# Les modèles proxy

class RestoProxy(Restaurant):
    class Meta:
        proxy = True  # Nous spécifions qu'il s'agit d'un proxy
        ordering = ["nom"]  # Nous changeons le tri par défaut

    def crepes(self):
        if "crêpe" in self.menu:  # Il y a des crêpes dans le menu
            return True
        return False




class Commentaire(models.Model):
    auteur = models.CharField(max_length=255)
    contenu = models.TextField()
    content_type = models.ForeignKey(ContentType,  on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "Commentaire de {0} sur {1}".format(self.auteur, self.content_object)


class Eleve(models.Model):
    nom = models.CharField(max_length=31)
    moyenne = models.IntegerField(default=10)
    commentaires = GenericRelation(Commentaire,
                                   content_type_field="le_champ_du_content_type",
                                   object_id_field="le champ_de_l_id")


    def __str__(self):
        return "Élève {0} ({1}/20 de moyenne)".format(self.nom, self.moyenne)


class Cours(models.Model):
    nom = models.CharField(max_length=31)
    eleves = models.ManyToManyField(Eleve)

    def __str__(self):
        return self.nom

"""
les signeaux
"""
"""
from django.db.models.signals import post_delete
from django.dispatch import receiver

@receiver(post_delete, sender=MonModele)
def ma_fonction_de_suppression(sender, instance, **kwargs):
	# processus de suppression selon les données fournies par instance
"""
#créer un nouveau signal

from django.dispatch import Signal

crepe_finie = Signal(providing_args=["adresse", "prix"])

#crepe_finie.connect(faire_livraison)   # Quand crepe_finie est lancé, appeler 'faire_livraison'

class Crepe(models.Model):
	nom_recette = models.CharField(max_length=255)
	prix = models.IntegerField()
	# ...

	def preparer(self, adresse):
		# Nous préparons la crêpe pour l'expédier à l'adresse transmise
		crepe_finie.send(sender=self, adresse=adresse, prix=self.prix)


