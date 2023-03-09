from django.db import models
from django.urls import reverse
from category.models import Category
from accounts.models import Account


class Product(models.Model):
    """Product model class
    
    Attributes:
        title (CharField): A field for the title of the product.
        slug (SlugField): A slug field to create unique product URL.
        description (TextField): A field to describe the product.
        price (DecimalField): A field to store the price of the product.
        images (ImageField): A field to store product images.
        stock (IntegerField): A field to store the stock quantity of the product.
        is_available (BooleanField): A field to mark if the product is available or not.
        category (ForeignKey): A foreign key reference to the category the product belongs to.
        created_date (DateTimeField): A field to store the date and time the product was created.
        modified_date (DateTimeField): A field to store the date and time the product was last modified.
    """
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
        """Returns the URL of the product."""
        
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self) -> str:
        return self.title
    

class VariationManager(models.Manager):
    """Django variations model manager"""
    def colors(self):
        """Returns a queryset of color variations of a product."""
        return super(VariationManager, self).filter(category='color', is_active=True)
    
    def sizes(self):
        """Returns a queryset of size variations of a product."""
        return super(VariationManager, self).filter(category='size', is_active=True)


class Variations(models.Model):
    """Variations model class
    
    Attributes:
        product (ForeignKey): A foreign key reference to the product for which the variation is being added.
        category (CharField): A field to store the category of the variation (e.g., color, size).
        value (CharField): A field to store the value of the variation (e.g., red, large).
        is_active (BooleanField): A field to mark if the variation is active or not.
        created_date (DateTimeField): A field to store the date and time the variation was created.
    """
    VARIATIONS_CATEGORY_CHOICES = (
        ('color', 'color'),
        ('size', 'size'),
    )

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


class ReviewRating(models.Model):
    """Review rating model class.

    Attributes:
        product (ForeignKey): A foreign key reference to the product for which the review is being added.
        user (ForeignKey): A foreign key reference to the user who added the review.
        subject (CharField): A field to store the subject of the review.
        review (TextField): A field to store the review text.
        rating (FloatField): A field to store the rating given by the user.
        ip (CharField): A field to store the IP address of the user who added the review.
        status (BooleanField): A field to mark if the review is active or not.
        created_at (DateTimeField): A field to store the date and time the review was created.
        updated_at (DateTimeField): A field to store the date and time the review was last modified.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.subject
