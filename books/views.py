from django.shortcuts import redirect, render
from .models import Book, ViewBook
from django.contrib.messages import constants
from django.contrib import messages


def create_books(request):
    if request.method == "GET":
        books = Book.objects.filter(user=request.user)

        views_totais = ViewBook.objects.filter(book__user=request.user).count()
        print(views_totais)
        return render(
            request, "create_books.html", {
                "books": books,
                "views_totais": views_totais}
        )

    elif request.method == "POST":
        title = request.POST.get("title")
        file = request.FILES["file"]

        book = Book(user=request.user, title=title, file=file)

        book.save()
        messages.add_message(
            request, constants.SUCCESS,
            "Apostila Salva com Sucesso")
        return redirect("/books/create_books/")


def book(request, id):
    if request.method == "GET":
        book = Book.objects.get(id=id)
        view_totais = ViewBook.objects.filter(book=book).count()
        single_view = ViewBook.objects.filter(
            book=book
            ).values('ip').distinct().count()
        view = ViewBook(ip=request.META["REMOTE_ADDR"], book=book)
        view.save()
        return render(request, 'book.html', {
            'book': book,
            'view_totais': view_totais,
            'single_view': single_view
            })
