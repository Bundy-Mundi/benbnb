from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models


class LoginForms(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        try:
            user = models.User.objects.get(username=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Wrong password"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User doesn't exist"))


class SignUpForms(forms.ModelForm):
    """ Sign Up Forms Definition """

    class Meta:

        model = models.User
        fields = ("first_name", "last_name", "email")
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password Confirmation"})
    )

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("Password doesn't match")
        else:
            return password

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            user = models.User.objects.get(username=email)
            if user is not None:
                raise forms.ValidationError("This email has been using by others")
        except models.User.DoesNotExist:
            return email

    def save(self, *args, **kwargs):

        # ModelForm saves object automatically, but doesn't care about that
        # username is email and creating password.
        # So in here, we are configuring it manually.
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        email = self.cleaned_data.get("email")
        user.username = email
        user.set_password(password)
        user.save()

