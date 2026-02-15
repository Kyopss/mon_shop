from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['full_name', 'email', 'address1', 'city', 'state', 'zipcode']
        # On exclut 'user' car on le remplira automatiquement avec l'utilisateur connecté

        # On stylise les champs pour qu'ils ressemblent à ton template Bootstrap
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom et Nom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'vous@exemple.com'}),
            'address1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123 rue des Lilas'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Paris'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'France'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '75000'}),
        }
        
        # On change les étiquettes pour le français
        labels = {
            'full_name': 'Nom complet',
            'email': 'Email',
            'address1': 'Adresse',
            'city': 'Ville',
            'state': 'Pays / Région',
            'zipcode': 'Code Postal',
        }