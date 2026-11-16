from django.urls import path

from . import views

app_name = "frontend"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("questions/", views.question_list, name="question_list"),
    path("questions/new/", views.question_create, name="question_create"),
    path("questions/<int:pk>/", views.question_detail, name="question_detail"),
    path("questions/<int:pk>/comment/", views.add_comment, name="add_comment"),
    path("questions/<int:pk>/favorite/", views.toggle_favorite, name="toggle_favorite"),
    path("questions/<int:pk>/review/", views.toggle_review, name="toggle_review"),
    path("questions/<int:pk>/moderate/", views.moderate_question, name="moderate_question"),
    path("questions/<int:pk>/delete/", views.delete_question, name="delete_question"),
    path("comments/<int:pk>/delete/", views.delete_comment, name="delete_comment"),
    path("favorites/", views.favorites, name="favorites"),
    path("review-list/", views.review_list, name="review_list"),
    path("feed/", views.feed, name="feed"),
    path("profile/", views.profile, name="profile"),
    path("users/<int:pk>/", views.user_profile, name="user_profile"),
    path("users/<int:pk>/subscribe/", views.toggle_subscribe, name="toggle_subscribe"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
