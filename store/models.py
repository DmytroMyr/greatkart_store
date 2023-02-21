from django.db import models
from django.urls import reverse
from category.models import Category


class Product(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self) -> str:
        """Getting product url"""
        
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self) -> str:
        return self.title
    

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(category='color', is_active=True)
    
    def sizes(self):
        return super(VariationManager, self).filter(category='size', is_active=True)


VARIATIONS_CATEGORY_CHOICES = (
    ('color', 'color'),
    ('size', 'size'),
)


class Variations(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, choices=VARIATIONS_CATEGORY_CHOICES)
    value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()

    class Meta:
        verbose_name = 'variations'
        verbose_name_plural = 'variations'

    def __str__(self) -> str:
        return self.value
