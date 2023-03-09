from django import forms
from django.core.validators import EmailValidator
from .models import Account


class RegistrationForm(forms.ModelForm):
    """Registration form model.
    
    Attributes:
        email (EmailField): A field to capture the email address of the user.
        password (CharField): A field to capture the password of the user.
        confirm_password (CharField): A field to confirm the password of the user.
    """
    email = forms.EmailField(widget=forms.PasswordInput(attrs={
        'type': 'email',
    }), validators=[EmailValidator(message="Invalid email address")])
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password',
        'class': 'form-control',
    }))

    class Meta:
        model = Account
        fields = ('username', 'email', 'password')

    def clean(self):
        """Custom password validation that raises a validation error if passwords don't match."""
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Password does not match.')
        
    def clean_email(self):
        """Custom email validation that raises a validation error if the email already exists in the database.
        
        Returns:
            email (str): The email address entered by the user.
        """
        email = self.cleaned_data['email']
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email
    
    def clean_username(self):
        """Custom username validation that raises a validation error if the username is less than 4 characters long.

        Returns:
            username (str): The username entered by the user.
        """
        username = self.cleaned_data['username']
        if len(username) < 4:
            raise forms.ValidationError('Username must be at least 4 characters long.')
        return username

    def clean_password(self):
        """Custom password validation that raises a validation error if the password is less than 4 characters long.

        Returns:
            password (str): The password entered by the user.
        """
        password = self.cleaned_data.get('password')

        if len(password) < 4:
            raise forms.ValidationError('Password must be at least 4 characters long.')
            
        return password

    def __init__(self, *args, **kwargs):
         super(RegistrationForm, self).__init__(*args, **kwargs)

         for field in self.fields:
             self.fields[field].widget.attrs['class'] = 'form-control'
