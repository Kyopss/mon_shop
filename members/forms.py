from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre Email'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        # On ajoute les classes Bootstrap aux champs générés automatiquement
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pseudo'}),
        }

    # Cette petite boucle magique ajoute la classe 'form-control' à tous les champs
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'