from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CommentViewSet, QuestionViewSet, TopicViewSet, UserViewSet, download_review_list

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("topics", TopicViewSet, basename="topic")
router.register("questions", QuestionViewSet, basename="question")
router.register("comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("review_list/download/", download_review_list, name="review-list-download"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
