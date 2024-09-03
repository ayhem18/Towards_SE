from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label="Your username", max_length=50, required=True)
    password = forms.CharField(label="Your password", min_length=6, required=True, widget=forms.PasswordInput)
    repeated_password = forms.CharField(label="Confirm Your password", min_length=6, required=True, widget=forms.PasswordInput)
    email = forms.EmailField(label="Your email", required=True)

    first_name = forms.CharField(label="Your first name", max_length=50, required=True)
    last_name = forms.CharField(label="Your last name", max_length=50, required=True)

    def is_valid(self) -> bool:
        if not super().is_valid():
            return False
        
        # the self.cleaned_data can (should?) only be used after calling the super().is_valid function 
        
        # make sure the password is entered correctly twice !!!
        return self.cleaned_data['password'] == self.cleaned_data['repeated_password']


from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Your username", max_length=50, required=True)
    password = forms.CharField(label="Your password", min_length=6, required=True, widget=forms.PasswordInput)

