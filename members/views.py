from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from payment.models import Order

# 1. CONNEXION
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Vous êtes connecté !")
            return redirect('store:product_all') # Retour à l'accueil
        else:
            messages.success(request, "Erreur : Identifiant ou mot de passe incorrect.")
            return redirect('login')
    else:
        return render(request, 'members/login.html')

# 2. DÉCONNEXION
def logout_user(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté.")
    return redirect('store:product_all')

# 3. INSCRIPTION
def register_user(request):
    if request.method == 'POST':
        # On utilise notre formulaire personnalisé ici
        form = SignUpForm(request.POST) 
        if form.is_valid():
            form.save()
            messages.success(request, "Compte créé avec succès ! Connectez-vous.")
            return redirect('login')
        else:
            # S'il y a une erreur, on l'affiche
            messages.success(request, "Erreur dans le formulaire. Vérifiez les champs.")
    else:
        form = SignUpForm()

    return render(request, 'members/register.html', {'form': form})

def user_orders(request):
    if request.user.is_authenticated:
        # On récupère toutes les commandes de l'utilisateur, de la plus récente à la plus ancienne
        orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
        return render(request, 'members/user_orders.html', {'orders': orders})
    else:
        messages.success(request, "Veuillez vous connecter pour voir vos commandes.")
        return redirect('login')