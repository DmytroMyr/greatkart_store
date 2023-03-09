from django.db import models
from store.models import Product, Variations
from accounts.models import Account


class Cart(models.Model):
    """A model representing a shopping cart.

    Attributes:
        cart_id (str): The unique identifier for the shopping cart.
        date_added (datetime): The datetime when the shopping cart was created.
    """
    cart_id = models.CharField(max_length=255, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    

class CartItem(models.Model):
    """A model representing an item in a shopping cart.

    Attributes:
        user (Account): The user who added the item to the shopping cart.
        product (Product): The product that was added to the shopping cart.
        variation (Variations): The variation(s) selected for the product.
        cart (Cart): The shopping cart containing the item.
        quantity (int): The quantity of the product in the shopping cart.
        is_active (bool): Whether the item is active.
    """
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variations, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self) -> int:
        """Calculate the total price of the item.

        Returns:
            int: The total price of the item.
        """
        return self.product.price * self.quantity

    def __unicode__(self):
        """Return the name of the product."""
        return self.product
    
