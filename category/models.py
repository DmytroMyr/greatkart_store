from django.db import models
from django.urls import reverse


class Category(models.Model):
    """A model representing a category for products.

    Attributes:
        title (str): The name of the category.
        slug (str): The slugified version of the title for use in URLs.
        description (str): A brief description of the category.
        image (File): An image representing the category.
    """
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    image = models.ImageField(upload_to='photos/categories/', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self) -> str:
        """Get the URL of the category page.

        Returns:
            str: The URL of the category page.
        """
        return reverse('products_by_category', args=[self.slug])

    def __str__(self) -> str:
        return self.title
