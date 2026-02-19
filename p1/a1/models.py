from django.db import models

class user(models.Model):
    name = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    @property
    def display_id(self):
        return User.objects.filter(id__lte=self.id).count()


# Create your models here.
