from django.http import HttpResponse
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
            return redirect("/users/logar")
        except:
            messages.add_message(
                request, constants.ERROR, " Erro Interno, refaça a solicitação"
            )
            return redirect("/users/register")


def create_super_user(request):
    if request.method == "GET":
        return render(request, "create_super_user.html")
    elif request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        is_staff = request.POST.get("is_staff")

        if not password == confirm_password:
            messages.add_message(request, constants.ERROR, " senhas não coíncidem")
            return redirect("/users/create_super_user")

        user = User.objects.filter(username=username)
        if user.exists():
            messages.add_message(request, constants.ERROR, " Usuários já existe")
            return redirect("/users/create_super_user")
        # ...

    try:
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password,
            is_staff=is_staff,
        )

        messages.add_message(
            request, constants.SUCCESS, "Usuário cadastrado com sucesso"
        )
        return redirect("/users/create_super_user")
    except Exception as e:
        messages.add_message(
            request, constants.ERROR, "Erro Interno, refaça a solicitação"
        )
        return redirect("/users/create_super_user")


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
