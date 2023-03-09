from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, User


class MyAccountManager(BaseUserManager):
    """Django custom user model manager."""

    def create_user(self, username: str, email: str, password: str = None) -> User:
        """Create and save a new user with the given email, username, and password.

        Args:
            username (str): The username of the user.
            email (str): The email address of the user.
            password (str, optional): The password of the user. Defaults to None.

        Raises:
            ValueError: If the email or username is not provided.

        Returns:
            User: The newly created user object.
        """
        if not email:
            raise ValueError('User must have an email address.')
        
        if not username:
            raise ValueError('User must have an username address.')
        
        user: User = self.model(
            email = self.normalize_email(email),
            username = username,
        )

        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username: str, email: str, password: str = None) -> User:
        """Create and save a new superuser with the given email, username, and password.

        Args:
            username (str): The username of the superuser.
            email (str): The email address of the superuser.
            password (str, optional): The password of the superuser. Defaults to None.

        Returns:
            User: The newly created superuser object.
        """
        user: User = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
        )

        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    """A custom user model that uses email as the unique identifier instead of username.

    Attributes:
        username (str): The username of the user.
        email (str): The email address of the user.
        date_joined (datetime): The datetime when the user was created.
        last_login (datetime): The datetime when the user last logged in.
        is_staff (bool): Whether the user is a staff member.
        is_active (bool): Whether the user account is active.
        is_superuser (bool): Whether the user is a superuser.
        USERNAME_FIELD (str): The field used as the unique identifier for the user.
        REQUIRED_FIELDS (list): The list of required fields for creating a user.

    """
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

