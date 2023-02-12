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
    # on appel resige_image()
    # super() assure la compatibilité entre cette méthode et la méthode d'origine
    # RESULTAT : Toutes les photos seront redimensionnées avant d'être sauvegardées !
    def save(self, *args, **kwargs):
        self.resize_image()
        super().save(*args, **kwargs)


class Blog(models.Model):
    photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, blank=True)
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=5000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    starred = models.BooleanField(default=False)
    word_count = models.IntegerField(default=0)

    def _get_word_count(self):
        return len(self.content.split())

    def save(self, *args, **kwargs):
        self.word_count = self._get_word_count()
        super().save(*args, **kwargs)
