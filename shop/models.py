from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length=50)
  slug = models.SlugField(max_length=200, unique=True)

  class Meta:
    ordering = ('name', )
    verbose_name = 'category'
    verbose_name_plural = 'catergories'

  def __str__(self):
    return self.name

class Product(models.Model):
  name = models.CharField(max_length=200)
  img = models.ImageField(upload_to='products/images', blank=True)
  price = models.DecimalField(max_digits=6, decimal_places=2)
  stock = models.IntegerField(default=0)
  description = models.TextField()
  slug = models.SlugField(max_length=200, unique=True)
  manufactured_on = models.DateTimeField()
  category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
  features = RichTextField(blank=True)

  class Meta:
    ordering = ('name', )
    verbose_name = 'product'
    verbose_name_plural = 'products'

  def __str__(self):
    return self.name