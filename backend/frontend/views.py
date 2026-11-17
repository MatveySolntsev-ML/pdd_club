from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.validators import validate_image_file_extension
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from PIL import Image, UnidentifiedImageError

from favorites.models import Favorite, ReviewList
from questions.models import Comment, Question, Topic
from subscriptions.models import Subscription

User = get_user_model()


def validate_uploaded_image(f):
    """Reject anything that isn't a genuine, safely-extensioned image file."""
    if f is None:
        return None
    validate_image_file_extension(f)
    try:
        Image.open(f).verify()
    except UnidentifiedImageError:
        raise ValidationError("Файл не распознан как изображение.")
    finally:
        f.seek(0)
    return f

TOPIC_COLORS = ["#2563eb", "#d946ef", "#f59e0b", "#16a34a", "#dc2626", "#0891b2", "#7c3aed", "#ea580c"]


def topic_color(topic_id):
    return TOPIC_COLORS[topic_id % len(TOPIC_COLORS)]


def _attach_colors(questions):
    for q in questions:
        q.topic_color = topic_color(q.topic_id)
    return questions


def _user_flags(request, questions):
    if not request.user.is_authenticated:
        return set(), set()
    ids = [q.id for q in questions]
    fav_ids = set(Favorite.objects.filter(user=request.user, question_id__in=ids).values_list("question_id", flat=True))
    rev_ids = set(ReviewList.objects.filter(user=request.user, question_id__in=ids).values_list("question_id", flat=True))
    return fav_ids, rev_ids


def landing(request):
    stats = {
        "questions": Question.objects.count(),
        "topics": Topic.objects.count(),
        "users": User.objects.count(),
        "comments": Comment.objects.count(),
    }
    recent = list(Question.objects.select_related("author", "topic").order_by("-created_at")[:3])
    _attach_colors(recent)
    return render(request, "frontend/landing.html", {"stats": stats, "recent": recent})


def question_list(request):
    questions = Question.objects.select_related("author", "topic").order_by("-created_at")
    topic_slug = request.GET.get("topic")
    current_topic = None
    if topic_slug:
        questions = questions.filter(topic__slug=topic_slug)
        current_topic = topic_slug
    questions = list(questions)
    _attach_colors(questions)
    favorite_ids, review_ids = _user_flags(request, questions)
    return render(request, "frontend/question_list.html", {
        "active_tab": "questions",
        "questions": questions,
        "topics": Topic.objects.all(),
        "current_topic": current_topic,
        "favorite_ids": favorite_ids,
        "review_ids": review_ids,
    })


def question_detail(request, pk):
    question = get_object_or_404(Question.objects.select_related("author", "topic"), pk=pk)
    comments = question.comments.select_related("author").all()
    is_favorite = is_in_review = can_moderate = can_delete_question = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, question=question).exists()
        is_in_review = ReviewList.objects.filter(user=request.user, question=question).exists()
        can_moderate = request.user.is_moderator
        can_delete_question = can_moderate or question.author_id == request.user.id
    return render(request, "frontend/question_detail.html", {
        "active_tab": "questions",
        "question": question,
        "topic_color": topic_color(question.topic_id),
        "comments": comments,
        "is_favorite": is_favorite,
        "is_in_review": is_in_review,
        "can_moderate": can_moderate,
        "can_delete_question": can_delete_question,
    })


@login_required
@require_POST
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if question.author_id != request.user.id and not request.user.is_moderator:
        messages.error(request, "Недостаточно прав для удаления этого вопроса.")
        return redirect("frontend:question_detail", pk=pk)
    question.delete()
    messages.success(request, "Вопрос удалён.")
    return redirect("frontend:question_list")


@login_required
@require_POST
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    question_id = comment.question_id
    if comment.author_id != request.user.id and not request.user.is_moderator:
        messages.error(request, "Недостаточно прав для удаления этого комментария.")
        return redirect("frontend:question_detail", pk=question_id)
    comment.delete()
    return redirect("frontend:question_detail", pk=question_id)


@login_required
def question_create(request):
    topics = Topic.objects.all()
    if request.method == "POST":
        topic = get_object_or_404(Topic, pk=request.POST.get("topic"))
        try:
            image = validate_uploaded_image(request.FILES.get("image"))
        except ValidationError as exc:
            messages.error(request, exc.messages[0])
            return render(request, "frontend/question_form.html", {"active_tab": "questions", "topics": topics})
        question = Question.objects.create(
            author=request.user,
            topic=topic,
            ticket_number=request.POST.get("ticket_number"),
            text=request.POST.get("text"),
            image=image,
        )
        return redirect("frontend:question_detail", pk=question.id)
    return render(request, "frontend/question_form.html", {"active_tab": "questions", "topics": topics})


@login_required
@require_POST
def add_comment(request, pk):
    question = get_object_or_404(Question, pk=pk)
    text = request.POST.get("text", "").strip()
    if text:
        Comment.objects.create(question=question, author=request.user, text=text)
    return redirect("frontend:question_detail", pk=pk)


@login_required
@require_POST
def toggle_favorite(request, pk):
    question = get_object_or_404(Question, pk=pk)
    obj, created = Favorite.objects.get_or_create(user=request.user, question=question)
    if not created:
        obj.delete()
    return redirect(request.META.get("HTTP_REFERER") or "frontend:question_list")


@login_required
@require_POST
def toggle_review(request, pk):
    question = get_object_or_404(Question, pk=pk)
    obj, created = ReviewList.objects.get_or_create(user=request.user, question=question)
    if not created:
        obj.delete()
    return redirect(request.META.get("HTTP_REFERER") or "frontend:question_list")


@login_required
@require_POST
def moderate_question(request, pk):
    if not request.user.is_moderator:
        messages.error(request, "Только модератор может менять статус вопроса.")
        return redirect("frontend:question_detail", pk=pk)
    question = get_object_or_404(Question, pk=pk)
    question.status = Question.STATUS_OPEN if question.status == Question.STATUS_RESOLVED else Question.STATUS_RESOLVED
    question.save(update_fields=["status"])
    return redirect("frontend:question_detail", pk=pk)


@login_required
def favorites(request):
    questions = list(Question.objects.select_related("author", "topic").filter(favorited_by__user=request.user).order_by("-created_at"))
    _attach_colors(questions)
    favorite_ids, review_ids = _user_flags(request, questions)
    return render(request, "frontend/list_page.html", {
        "active_tab": "favorites", "title": "Избранное", "questions": questions,
        "favorite_ids": favorite_ids, "review_ids": review_ids,
        "empty_text": "Вы ещё не добавили вопросы в избранное.",
    })


@login_required
def review_list(request):
    questions = list(Question.objects.select_related("author", "topic").filter(in_review_lists__user=request.user).order_by("-created_at"))
    _attach_colors(questions)
    favorite_ids, review_ids = _user_flags(request, questions)
    return render(request, "frontend/list_page.html", {
        "active_tab": "review", "title": "Список на повторение", "questions": questions,
        "favorite_ids": favorite_ids, "review_ids": review_ids,
        "download_url": "/api/review_list/download/",
        "empty_text": "Список на повторение пуст.",
    })


@login_required
def feed(request):
    authors = User.objects.filter(subscribers__follower=request.user)
    questions = list(Question.objects.select_related("author", "topic").filter(author__in=authors).order_by("-created_at"))
    _attach_colors(questions)
    favorite_ids, review_ids = _user_flags(request, questions)
    return render(request, "frontend/list_page.html", {
        "active_tab": "feed", "title": "Лента подписок", "questions": questions,
        "favorite_ids": favorite_ids, "review_ids": review_ids,
        "empty_text": "Вы пока ни на кого не подписаны — зайдите в профиль автора на странице вопроса.",
    })


def user_profile(request, pk):
    profile_user = get_object_or_404(User, pk=pk)
    questions = list(Question.objects.select_related("topic").filter(author=profile_user).order_by("-created_at"))
    _attach_colors(questions)
    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = Subscription.objects.filter(follower=request.user, author=profile_user).exists()
    return render(request, "frontend/user_profile.html", {
        "profile_user": profile_user,
        "questions": questions,
        "questions_count": len(questions),
        "subscribers_count": Subscription.objects.filter(author=profile_user).count(),
        "is_following": is_following,
    })


@login_required
@require_POST
def toggle_subscribe(request, pk):
    author = get_object_or_404(User, pk=pk)
    if author != request.user:
        obj, created = Subscription.objects.get_or_create(follower=request.user, author=author)
        if not created:
            obj.delete()
    return redirect("frontend:user_profile", pk=pk)


@login_required
def profile(request):
    subscriptions = User.objects.filter(subscribers__follower=request.user)
    return render(request, "frontend/profile.html", {
        "active_tab": "profile",
        "profile_user": request.user,
        "questions_count": Question.objects.filter(author=request.user).count(),
        "subscriptions": subscriptions,
    })


def register(request):
    errors = {}
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")
        if not username:
            errors["username"] = "Обязательное поле"
        elif User.objects.filter(username=username).exists():
            errors["username"] = "Имя пользователя занято"
        if not email:
            errors["email"] = "Обязательное поле"
        elif User.objects.filter(email=email).exists():
            errors["email"] = "Этот email уже зарегистрирован"
        if not password1 or len(password1) < 8:
            errors["password1"] = "Минимум 8 символов"
        if password1 != password2:
            errors["password2"] = "Пароли не совпадают"
        if not errors:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            return redirect("frontend:question_list")
        return render(request, "frontend/register.html", {"errors": errors, "posted": request.POST})
    return render(request, "frontend/register.html", {"errors": errors, "posted": {}})


def login_view(request):
    error = None
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
        if user is not None:
            login(request, user)
            return redirect("frontend:question_list")
        error = "Неверное имя пользователя или пароль."
    return render(request, "frontend/login.html", {"error": error})


@require_POST
def logout_view(request):
    logout(request)
    return redirect("frontend:question_list")
