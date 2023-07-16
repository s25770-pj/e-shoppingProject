import os
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import ValidationError
from django.utils.deconstruct import deconstructible


class Category(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_product_count(self):
        return Product.objects.filter(category=self).count


@deconstructible
class ProductImageUploadPath:

    def __init__(self, subfolder):
        self.subfolder = subfolder

    def __call__(self, instance, filename):
        ext = os.path.splitext(filename)[1]
        new_filename = f"{instance.name}{ext}"
        return os.path.join(self.subfolder, new_filename)

    def deconstruct(self):
        return (self.__class__.__name__,['{self.subfolder}'])



def validate_min_resolution(image):
    min_width = 600
    min_height = 600

    if image.width < min_width or image.height < min_height:
        raise ValidationError(f"The image resolution should be at least {min_width}x{min_height} pixels.")


class Product(models.Model):
    objects = models.Manager()
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to=ProductImageUploadPath('static/images/'),
                              validators=[validate_min_resolution]
                              )

    class Meta:
        ordering = ['created', 'updated']

    def __str__(self):
        return self.name


class Comment(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    body = models.TextField(null=False, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]


class Settings(models.Model):
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark Theme'),
    ]

    LANGUAGE_CHOICES = [
        ('pl', 'Polish'),
        ('en', 'English'),
    ]
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notifications_enabled = models.BooleanField(default=False)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en', null=False)
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light', null=False)

    def __str__(self):
        return f"Settings for {self.user.username}"
