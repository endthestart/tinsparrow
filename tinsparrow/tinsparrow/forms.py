from django import forms
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    """
    Form for to log in to the site.
    """
    email = forms.EmailField(label=_("Email"))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    user = None

    error_messages = {
        'invalid_login': _("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive."),
        'no_cookies': _("Your Web browser doesn't appear to have cookies "
                        "enabled. Cookies are required for logging in."),
        'inactive': _("This account is inactive."),
    }

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(username=self.data['email'],
                                password=self.data['password'])
            if user is not None:
                if user.is_active:
                    self.user = user
                else:
                    raise forms.ValidationError(_("This account is currently inactive."))
            else:
                raise forms.ValidationError(_("The user name and password you supplied is not valid."))

    def login(self, request):
        if self.is_valid():
            login(request, self.user)
            return True
        return False
