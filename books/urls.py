from django.urls import path
from . import views

urlpatterns = [
    path('create_books/', views.create_books, name='create_books'),
    path('book/<int:id>', views.book, name='book')
]
