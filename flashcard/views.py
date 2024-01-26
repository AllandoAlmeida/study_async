from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from .models import Category, Challenge, Flashcard, FlashcardChallenge
from django.contrib.messages import constants
from django.contrib import messages


# Create your views here.
def new_flashcard(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect("/users/logar")
        else:
            categories = Category.objects.all()
            difficulties = Flashcard.DIFFICULTY_CHOICES
            flashcards = Flashcard.objects.filter(user=request.user)

            category_filter = request.GET.get("category")
            difficulty_filter = request.GET.get("difficulty")

            if category_filter:
                flashcards = flashcards.filter(category__id=category_filter)

            if difficulty_filter:
                flashcards = flashcards.filter(difficulty=difficulty_filter)

            if len(flashcards) == 0:
                messages.add_message(
                    request,
                    constants.INFO,
                    "Não há dados para os critérios selecionados",
                )

            return render(
                request,
                "new_flashcard.html",
                {
                    "categories": categories,
                    "difficulties": difficulties,
                    "flashcards": flashcards,
                },
            )
    elif request.method == "POST":
        question = request.POST.get("question")
        result = request.POST.get("result")
        category = request.POST.get("category")
        difficulty = request.POST.get("difficulty")

        if (
            not question
            or not result
            or len(question.strip()) == 0
            or len(result.strip()) == 0
        ):
            messages.add_message(
                request,
                constants.ERROR,
                "Preencha os campos de pergunta e resposta",
            )
            return redirect("/flashcard/new_flashcard")

        flashcard = Flashcard(
            user=request.user,
            question=question,
            result=result,
            category_id=category,
            difficulty=difficulty,
        )

        flashcard.save()
        messages.add_message(
            request, constants.SUCCESS, "Flashcard criada com sucesso!"
        )
        return redirect("/flashcard/new_flashcard")


def deletar_flashcard(request, id):
    try:
        flashcard = Flashcard.objects.get(id=id)
    except Flashcard.DoesNotExist:
        messages.add_message(request, constants.ERROR, "Flashcard não existe")
        return redirect("/flashcard/new_flashcard")

    if not flashcard.user == request.user:
        messages.add_message(request, constants.ERROR, "Operação não realizada!")
        return redirect("/flashcard/new_flashcard")
    else:
        flashcard.delete()
        messages.add_message(
            request, constants.SUCCESS, "Flashcard deletado com Sucesso!"
        )
        return redirect("/flashcard/new_flashcard")


def start_challenges(request):
    if request.method == "GET":
        categories = Category.objects.all()
        difficulties = Flashcard.DIFFICULTY_CHOICES
        flashcards = Flashcard.objects.filter(user=request.user)

        return render(
            request,
            "start_challenges.html",
            {
                "categories": categories,
                "difficulties": difficulties,
                "flashcards": flashcards,
            },
        )
    elif request.method == "POST":
        title = request.POST.get("title")
        categories = request.POST.getlist("category")
        difficulty = request.POST.get("difficulty")
        quantity_questions = request.POST.get("quantity_questions")

        challenge = Challenge(
            user=request.user,
            title=title,
            quantity_questions=quantity_questions,
            difficulty=difficulty,
        )

        challenge.save()

        challenge.category.add(*categories)

        flashcards = (
            Flashcard.objects.filter(user=request.user)
            .filter(difficulty=difficulty)
            .filter(category_id__in=categories)
            .order_by("?")
        )

        if flashcards.count() < int(quantity_questions):
            messages.add_message(
                request,
                constants.ERROR,
                f"existem somente {flashcards.count()} disponiveis!",
            )
            return redirect("/flashcard/start_challenges/")

        flashcards = flashcards[: int(quantity_questions)]

        for flash in flashcards:
            flashcardChallenge = FlashcardChallenge(flashcard=flash)
            flashcardChallenge.save()
            challenge.flashcards.add(flashcardChallenge)

        challenge.save()

        return redirect("/flashcard/list_challenges/")


def list_challenges(request):
    if request.method == "GET":
        challenges = Challenge.objects.filter(user=request.user)
        categories = Category.objects.all()
        difficulties = Flashcard.DIFFICULTY_CHOICES
        flashcards = Flashcard.objects.filter(user=request.user)

        return render(
            request,
            "list_challenges.html",
            {
                "categories": categories,
                "difficulties": difficulties,
                "flashcards": flashcards,
                "challenges": challenges,
            },
        )


def challenges(request, id):
    challenge = Challenge.objects.get(id=id)
    if not challenge.user == request.user:
        return HttpResponseForbidden()

    if request.method == "GET":
        hits = (
            challenge.flashcards.filter(answered=True).filter(got_it_right=True).count()
        )
        wrong = (
            challenge.flashcards.filter(answered=True)
            .filter(got_it_right=False)
            .count()
        )

        need_to_respond = (
            challenge.flashcards.filter(answered=False)
            .filter(got_it_right=False)
            .count()
        )

        return render(
            request,
            "challenge.html",
            {
                "challenge": challenge,
                "hits": hits,
                "wrong": wrong,
                "need_to_respond": need_to_respond,
            },
        )


def challenge_send_answer(request, id):
    flashcard_challenge = FlashcardChallenge.objects.get(id=id)
    challenge_answer = request.GET.get("challenge_answer")
    challenge_id = request.GET.get("challenge_id")

    if not flashcard_challenge.flashcard.user == request.user:
        return HttpResponseForbidden()

    flashcard_challenge.answered = True

    flashcard_challenge.got_it_right = True if challenge_answer == "1" else False

    flashcard_challenge.save()

    return redirect(f"/flashcard/challenges/{challenge_id}")


def report(request, id):
    challenge = Challenge.objects.get(id=id)
    print("challenge", challenge)

    hits = challenge.flashcards.filter(got_it_right=True).count()

    wrong = (
        challenge.flashcards.filter(answered=True).filter(got_it_right=False).count()
    )

    data = [hits, wrong]

    categories = challenge.category.all()

    name_category = [i.name for i in categories]

    flash_by_category = []

    for category in categories:
        flash_by_category.append(
            challenge.flashcards.filter(flashcard__category=category)
            .filter(got_it_right=True)
            .count()
        )

    print(name_category)
    print(data)

    return render(
        request,
        "report.html",
        {
            "challenge": challenge,
            "data": data,
            "categories": name_category,
            "flash_by_category": flash_by_category,
        },
    )
