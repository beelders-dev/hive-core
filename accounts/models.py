import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    pass

    def get_initials(self):
        f_initial = self.first_name[:1]
        l_initial = self.last_name[:1]

        return f"{f_initial}{l_initial}".upper()
