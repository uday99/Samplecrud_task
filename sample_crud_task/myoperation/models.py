from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,UserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.



class Role(models.Model):
    id = models.IntegerField(primary_key=True,unique=True)
    Role_CHOICES = (
            ('A', 'admin'),
            ('M', 'manager'),
            ('S', 'staff')
            )
    role_name = models.CharField(max_length=4,choices=Role_CHOICES,unique=True)

    def __str__(self):
        return self.role_name




class Register(AbstractBaseUser):
    objects=UserManager()

    username=models.CharField(max_length=150,unique=True)
    email=models.CharField(max_length=100,unique=True)
    role=models.ForeignKey(Role,on_delete=models.CASCADE)

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

class ProductModel(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=250)
    inventory_count=models.IntegerField()

