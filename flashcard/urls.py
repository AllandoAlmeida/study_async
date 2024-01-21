from django.urls import path
from . import views

urlpatterns = [
    path("new_flashcard/", views.new_flashcard, name="new_flashcard"),
    path(
        "deletar_flashcard/<int:id>",
        views.deletar_flashcard,
        name="deletar_flashcard"
    ),
    path("start_challenges/", views.start_challenges, name="start_challenges"),
    path("list_challenges/", views.list_challenges, name="list_challenges"),
    path("challenges/<int:id>", views.challenges, name="challenges"),
    path(
        "challenge_send_answer/<int:id>",
        views.challenge_send_answer,
        name="challenge_send_answer"),
    path('report/<int:id>/', views.report, name='report')
]
