from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class UserChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = User
        field_classes = None


class UserCreationForm(auth_forms.UserCreationForm):
    error_message = auth_forms.UserCreationForm.error_messages.update(
        {"duplicate_email": _("An Account with this email already exists.")}
    )

    class Meta(auth_forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)
        field_classes = None

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise ValidationError(self.error_messages["duplicate_email"])


class CustomAuthenticationForm(auth_forms.AuthenticationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}), label=_("Email"), max_length=254)
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
