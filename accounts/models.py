from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    age = models.PositiveBigIntegerField(
        null=True, blank=True
    )  # null(database-related) -->puede almacenar una entrada de base de datos como nula, sin valor, blank(validation-related) --> true el formulario acepta un valor vacio, false un valor es requerido.
