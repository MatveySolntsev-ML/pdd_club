from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from favorites.models import Favorite, ReviewList
from questions.models import Question, Topic

User = get_user_model()


class FavoriteModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="vasya", email="vasya@example.com", password="x")
        self.author = User.objects.create_user(username="chef", email="chef@example.com", password="x")
        self.topic = Topic.objects.create(name="Знаки", slug="signs")
        self.question = Question.objects.create(
            author=self.author, topic=self.topic, ticket_number=1, text="Вопрос",
        )

    def test_favorite_unique_together(self):
        Favorite.objects.create(user=self.user, question=self.question)
        with self.assertRaises(IntegrityError):
            Favorite.objects.create(user=self.user, question=self.question)

    def test_review_list_unique_together(self):
        ReviewList.objects.create(user=self.user, question=self.question)
        with self.assertRaises(IntegrityError):
            ReviewList.objects.create(user=self.user, question=self.question)


class FavoriteActionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="vasya", email="vasya@example.com", password="x")
        self.author = User.objects.create_user(username="chef", email="chef@example.com", password="x")
        self.topic = Topic.objects.create(name="Знаки", slug="signs")
        self.question = Question.objects.create(
            author=self.author, topic=self.topic, ticket_number=1, text="Вопрос",
        )
        self.client.force_authenticate(user=self.user)

    def test_add_and_remove_favorite(self):
        response = self.client.post(f"/api/questions/{self.question.id}/favorite/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(f"/api/questions/{self.question.id}/favorite/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.delete(f"/api/questions/{self.question.id}/favorite/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_add_and_remove_review_list(self):
        response = self.client.post(f"/api/questions/{self.question.id}/review_list/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.delete(f"/api/questions/{self.question.id}/review_list/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_favorite_requires_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(f"/api/questions/{self.question.id}/favorite/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_download_review_list(self):
        self.client.post(f"/api/questions/{self.question.id}/review_list/")
        response = self.client.get("/api/review_list/download/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Билет 1", response.content.decode("utf-8"))

    def test_download_review_list_requires_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/review_list/download/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
