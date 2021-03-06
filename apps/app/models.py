from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField


class Category(MPTTModel):
    title = models.CharField(max_length=250)
    is_url = models.BooleanField(default=False)
    url = models.CharField(null=True, blank=True, max_length=250)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    tree = models.BooleanField(default=False, verbose_name='As tree ?')
    icon = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Brand(models.Model):
    title = models.CharField(max_length=250)
    category = TreeForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


class Slider(models.Model):
    image = models.ImageField(upload_to='sliders/')


class Content(models.Model):
    title = models.CharField(max_length=250)
    body = RichTextUploadingField()
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=60)
