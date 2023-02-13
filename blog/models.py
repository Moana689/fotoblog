from django.db import models
from django.conf import settings

from PIL import Image


class Photo(models.Model):
    image = models.ImageField()
    caption = models.CharField(max_length=128, blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (800, 600)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        # sauvegarde de l'image redimensionnée dans le système de fichiers
        # ATTENTION : ce n'est pas la méthode save() du modèle
        image.save(self.image.path)

    # override de la méthode Photo.save()
    # on reprend l'entête de la fonction d'origine
    # super() assure la compatibilité entre cette méthode et la méthode d'origine
    # on appel resige_image()
    # RESULTAT : Toutes les photo seront redimensionnées avant d'être sauvegarder !
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()


class Blog(models.Model):
    photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, blank=True)
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=5000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    starred = models.BooleanField(default=False)

    # TODO:check lib 'Django Guardian' et 'Rules' pour appliquer des permissions personnalisées aux instances
    # permission personnalisée
    # ATTENTION appliquée à un modèle uniquement !
    class Meta:
        permissions = [
            ('change_blig_title', 'Peut changer le titre d''un billet de blog')
        ]
