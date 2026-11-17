from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from core.permissions import IsAuthorOrModeratorOrReadOnly, IsModerator
from favorites.models import Favorite, ReviewList
from questions.models import Comment, Question, Topic
from subscriptions.models import Subscription

from .serializers import (
    CommentSerializer, FavoriteSerializer, QuestionModerateSerializer, QuestionSerializer,
    ReviewListSerializer, SubscriptionSerializer, TopicSerializer, UserProfileSerializer,
    UserRegistrationSerializer, UserSerializer,
)

User = get_user_model()


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegistrationSerializer
        if self.action in ("list", "retrieve", "subscriptions"):
            return UserProfileSerializer
        return UserSerializer

    @action(detail=False, methods=["get", "patch"], permission_classes=(IsAuthenticated,))
    def me(self, request):
        if request.method == "PATCH":
            serializer = UserSerializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response(UserSerializer(request.user).data)

    @action(detail=True, methods=["post", "delete"], permission_classes=(IsAuthenticated,))
    def subscribe(self, request, pk=None):
        author = self.get_object()
        if request.method == "POST":
            if author == request.user:
                return Response({"detail": "Нельзя подписаться на себя."}, status=status.HTTP_400_BAD_REQUEST)
            _, created = Subscription.objects.get_or_create(follower=request.user, author=author)
            if not created:
                return Response({"detail": "Уже подписаны."}, status=status.HTTP_400_BAD_REQUEST)
            return Response(SubscriptionSerializer(_).data, status=status.HTTP_201_CREATED)
        deleted, _ = Subscription.objects.filter(follower=request.user, author=author).delete()
        if not deleted:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"], permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        authors = User.objects.filter(subscribers__follower=request.user)
        return Response(UserSerializer(authors, many=True).data)


class TopicViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = (AllowAny,)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.select_related("author", "topic").all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthorOrModeratorOrReadOnly,)
    filterset_fields = ("topic", "ticket_number")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["get", "post"], permission_classes=(IsAuthenticatedOrReadOnly,))
    def comments(self, request, pk=None):
        question = self.get_object()
        if request.method == "POST":
            serializer = CommentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(question=question, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        page = self.paginate_queryset(question.comments.select_related("author"))
        serializer = CommentSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=["post", "delete"], permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk=None):
        question = self.get_object()
        if request.method == "POST":
            _, created = Favorite.objects.get_or_create(user=request.user, question=question)
            if not created:
                return Response({"detail": "Уже в избранном."}, status=status.HTTP_400_BAD_REQUEST)
            return Response(FavoriteSerializer(_).data, status=status.HTTP_201_CREATED)
        deleted, _ = Favorite.objects.filter(user=request.user, question=question).delete()
        if not deleted:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post", "delete"], url_path="review_list", permission_classes=(IsAuthenticated,))
    def review_list(self, request, pk=None):
        question = self.get_object()
        if request.method == "POST":
            _, created = ReviewList.objects.get_or_create(user=request.user, question=question)
            if not created:
                return Response({"detail": "Уже в списке на повторение."}, status=status.HTTP_400_BAD_REQUEST)
            return Response(ReviewListSerializer(_).data, status=status.HTTP_201_CREATED)
        deleted, _ = ReviewList.objects.filter(user=request.user, question=question).delete()
        if not deleted:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["patch"], permission_classes=(IsModerator,))
    def moderate(self, request, pk=None):
        question = self.get_object()
        serializer = QuestionModerateSerializer(question, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CommentViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModeratorOrReadOnly,)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_review_list(request):
    """GET /api/review_list/download/ — выгрузка списка вопросов на повторение в txt."""
    items = ReviewList.objects.filter(user=request.user).select_related("question")
    lines = [f"Билет {i.question.ticket_number}: {i.question.text}" for i in items]
    content = "\n\n".join(lines) or "Список на повторение пуст."
    response = HttpResponse(content, content_type="text/plain; charset=utf-8")
    response["Content-Disposition"] = "attachment; filename=review_list.txt"
    return response
