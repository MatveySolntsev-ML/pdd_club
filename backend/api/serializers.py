from django.contrib.auth import get_user_model
from rest_framework import serializers

from favorites.models import Favorite, ReviewList
from questions.models import Comment, Question, Topic
from subscriptions.models import Subscription

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "avatar", "role")
        read_only_fields = ("role",)


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    questions_count = serializers.IntegerField(source="questions.count", read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "avatar", "questions_count")


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ("id", "name", "slug")


class CommentSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "question", "author", "text", "created_at")
        read_only_fields = ("question", "author")


class QuestionSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    topic = TopicSerializer(read_only=True)
    topic_id = serializers.PrimaryKeyRelatedField(source="topic", queryset=Topic.objects.all(), write_only=True)

    class Meta:
        model = Question
        fields = (
            "id", "author", "topic", "topic_id", "ticket_number",
            "text", "image", "status", "created_at",
        )
        read_only_fields = ("author", "status")


class QuestionModerateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("status",)


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ("id", "user", "question")
        read_only_fields = ("user", "question")


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewList
        fields = ("id", "user", "question")
        read_only_fields = ("user", "question")


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("id", "follower", "author")
        read_only_fields = ("follower", "author")
