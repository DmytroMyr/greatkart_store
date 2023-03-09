from django.db import models
from accounts.models import Account
from store.models import Product, Variations


class Payment(models.Model):
    """A model representing a payment made by a user.

    Attributes:
        user (Account): The user who made the payment.
        payment_id (str): The ID of the payment.
        payment_method (str): The method used to make the payment.
        amount_paid (str): The amount of money paid.
        status (str): The status of the payment (e.g. "completed", "failed").
        created_at (datetime): The date and time the payment was created.
    """
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.payment_id
    

class Order(models.Model):
    """A class representing an Order in the e-commerce platform.

    Attributes:
        user (ForeignKey): A foreign key to the Account model representing the user who placed the order.
        payment (ForeignKey): A foreign key to the Payment model representing the payment made for the order.
        order_number (CharField): A string representing the unique order number.
        first_name (CharField): A string representing the first name of the person who placed the order.
        last_name (CharField): A string representing the last name of the person who placed the order.
        email (CharField): A string representing the email address of the person who placed the order.
        phone (CharField): A string representing the phone number of the person who placed the order.
        city (CharField): A string representing the city where the person who placed the order resides.
        address (CharField): A string representing the address where the person who placed the order resides.
        comment (CharField): A string representing any additional comments the person who placed the order provided.
        order_total (FloatField): A float representing the total amount of the order.
        tax (FloatField): A float representing the tax amount for the order.
        status (CharField): A string representing the current status of the order, selected from available options in STATUS.
        ip (CharField): A string representing the IP address from which the order was placed.
        is_ordered (BooleanField): A boolean indicating whether the order has been placed.
        created_at (DateTimeField): A datetime representing the date and time when the order was created.
        updated_at (DateTimeField): A datetime representing the date and time when the order was last updated.
    """
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cencelled', 'Cencelled'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    comment = models.CharField(max_length=255, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(max_length=20, blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self) -> str:
        """Returns a formatted string representing the full name of the person who placed the order."""
        return f'{self.first_name} {self.last_name}'
    
    def full_address(self) -> str:
        """Returns a formatted string representing the full address of the person who placed the order."""
        return f'{self.city}, {self.address}'

    def __str__(self) -> str:
        return self.first_name
    

class OrderProduct(models.Model):
    """Represents a product included in an order.

    Attributes:
        order (Order): The order that contains this product.
        payment (Payment): The payment associated with this product, if any.
        user (Account): The user who placed the order.
        product (Product): The product being ordered.
        variation (QuerySet): The variations of the product included in the order, if any.
        quantity (int): The number of products being ordered.
        product_price (Decimal): The price of the product, in dollars and cents.
        ordered (bool): Whether the product has been ordered.
        created_at (datetime): The date and time when this product was created.
        updated_at (datetime): The date and time when this product was last updated.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variations, blank=True)
    quantity = models.IntegerField()
    product_price = models.DecimalField(max_digits=6, decimal_places=2)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.product.title
