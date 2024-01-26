from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth


# Create your views here.
def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not password == confirm_password:
            messages.add_message(request, constants.ERROR, " senhas não coíncidem")
            return redirect("/users/register")

        user = User.objects.filter(username=username)
        if user.exists():
            messages.add_message(request, constants.ERROR, " Usuários já existe")
            return redirect("/users/register")
        try:
            User.objects.create_user(username=username, password=password)
            return redirect("/users/login")
        except:
            messages.add_message(
                request, constants.ERROR, " Erro Interno, refaza a solicitação"
            )
            return redirect("/users/register")


def logar(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/flashcard/new_flashcard/")
        else:
            return render(request, "login.html", {})
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

    user = auth.authenticate(request, username=username, password=password)

    if user:
        auth.login(request, user)
        messages.add_message(request, constants.SUCCESS, f"Bem vindo! {user}")
        print(user)
        return redirect("/flashcard/new_flashcard/", {"user": user})

    else:
        messages.add_message(request, constants.ERROR, "Usurname ou senha inválidos")

        return redirect("/users/logar")


def logout(request):
    auth.logout(request)

    messages.add_message(request, constants.INFO, "Logout realizado com sucesso")
    return redirect("/users/logar")
