from django import forms
from django.core.validators import EmailValidator, MinLengthValidator
from .models import Order


class OrderForm(forms.ModelForm):
    """Order form model"""
    email = forms.EmailField(validators=[EmailValidator(message="Invalid email address")])
    phone = forms.CharField(validators=[MinLengthValidator(10, message="Phone number must be at least 10 digits")])

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'phone', 'city', 'address', 'comment')

    def clean_first_name(self):
        """A method that cleans the first name field of a form.

        Args:
            self (object): The object instance.

        Returns:
            str: The cleaned first name.

        Raises:
            forms.ValidationError: If the first name contains any non-alphabetic characters.
        """
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("First name should only contain letters")
        return first_name

    def clean_last_name(self):
        """A method that cleans the last name field of a form.

        Args:
            self (object): The object instance.

        Returns:
            str: The cleaned last name.

        Raises:
            forms.ValidationError: If the last name contains any non-alphabetic characters.
        """
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("Last name should only contain letters")
        return last_name

    def clean_city(self):
        """A method that cleans the city field of a form.

        Args:
            self (object): The object instance.

        Returns:
            str: The cleaned city.

        Raises:
            forms.ValidationError: If the city contains any non-alphabetic characters.
        """
        city = self.cleaned_data.get('city')
        if not city.isalpha():
            raise forms.ValidationError("City name should only contain letters")
        return city

    def clean_comment(self):
        """
        A method that cleans the comment field of a form.

        Args:
            self (object): The object instance.

        Returns:
            str: The cleaned comment.

        Raises:
            forms.ValidationError: If the comment is longer than 200 characters.
        """
        comment = self.cleaned_data.get('comment')
        if len(comment) > 200:
            raise forms.ValidationError("Comment should be less than 200 characters")
        return comment
