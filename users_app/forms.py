from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
class Register(UserCreationForm):
    firstname = forms.CharField(max_length=200)
    lastname = forms.CharField(max_length=200)
    email = forms.EmailField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['firstname'].widget.attrs.update({'class':'input-group',
        'name':'firstname',
        'id':'firstname',
        'type':'text',
        'placeholder':'firstname'
        })
        self.fields['lastname'].widget.attrs.update({'class':'input-group',
        'name':'lastname',
        'id':'lastname',
        'type':'text',
        'placeholder':'lastname'
        })
        self.fields['username'].widget.attrs.update({'class':'input-group',
        'name':'username',
        'id':'username',
        'type':'text',
        'placeholder':'username'
        })
        self.fields['email'].widget.attrs.update({'class':'input-group',
        'name':'email',
        'id':'email',
        'type':'email',
        'placeholder':'email'
        })
        self.fields['password1'].widget.attrs.update({'class':'input-group',
        'name':'password1',
        'id':'password1',
        'type':'password',
        'placeholder':'password1',
        'minlength':'8'
        })
        self.fields['password2'].widget.attrs.update({'class':'input-group',
        'required':'', 
        'name':'password2',
        'id':'password2',
        'type':'password',
        'placeholder':'password2',
        'minlength':'8'
        })
    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'username','email','password1', 'password2']

    def clean_password(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if  password1 != password2:
            raise ValidationError({'password2':'password mismatch'})

        return password2

 
class CustomLoginForm(AuthenticationForm):
     def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class':'input-group',
        'name':'username',
        'id':'username',
        'type':'text',
        'placeholder':'username or email'
        })
        self.fields['password'].widget.attrs.update({'class':'input-group',
        'name':'password',
        'id':'password',
        'type':'text',
        'placeholder':'password'})


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']
