from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from questions.models import Comment, Question, Topic

User = get_user_model()


class QuestionModelTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="chef", email="chef@example.com", password="x")
        self.topic = Topic.objects.create(name="Знаки", slug="signs")

    def test_create_question(self):
        question = Question.objects.create(
            author=self.author, topic=self.topic, ticket_number=5, text="Что значит этот знак?",
        )
        self.assertEqual(question.status, Question.STATUS_OPEN)

    def test_create_comment(self):
        question = Question.objects.create(
            author=self.author, topic=self.topic, ticket_number=5, text="Вопрос",
        )
        comment = Comment.objects.create(question=question, author=self.author, text="Ответ")
        self.assertEqual(question.comments.count(), 1)
        self.assertEqual(comment.question, question)

    def test_topic_delete_protected_while_questions_exist(self):
        Question.objects.create(author=self.author, topic=self.topic, ticket_number=5, text="Вопрос")
        from django.db.models import ProtectedError
        with self.assertRaises(ProtectedError):
            self.topic.delete()


class QuestionPermissionTests(APITestCase):
    """The permission bug we found and fixed in Foodgram, checked here too:
    IsAuthorOrModeratorOrReadOnly alone only checks has_object_permission,
    so without IsAuthenticatedOrReadOnly alongside it, an anonymous POST
    could pass the permission check before crashing on an invalid author.
    """

    def setUp(self):
        self.author = User.objects.create_user(username="chef", email="chef@example.com", password="x")
        self.other = User.objects.create_user(username="other", email="other@example.com", password="x")
        self.topic = Topic.objects.create(name="Знаки", slug="signs")
        self.question = Question.objects.create(
            author=self.author, topic=self.topic, ticket_number=5, text="Вопрос",
        )

    def test_anonymous_cannot_create_question(self):
        response = self.client.post(
            "/api/questions/",
            {"topic_id": self.topic.id, "ticket_number": 1, "text": "Anon question"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Question.objects.filter(text="Anon question").exists())

    def test_authenticated_user_can_create_question(self):
        self.client.force_authenticate(user=self.other)
        response = self.client.post(
            "/api/questions/",
            {"topic_id": self.topic.id, "ticket_number": 1, "text": "Real question"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["author"]["id"], self.other.id)

    def test_non_author_cannot_edit_question(self):
        self.client.force_authenticate(user=self.other)
        response = self.client.patch(
            f"/api/questions/{self.question.id}/", {"text": "Hacked"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_author_can_edit_own_question(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.patch(
            f"/api/questions/{self.question.id}/", {"text": "Исправлено"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_moderator_can_edit_others_question(self):
        moderator = User.objects.create_user(
            username="mod", email="mod@example.com", password="x", role=User.ROLE_MODERATOR,
        )
        self.client.force_authenticate(user=moderator)
        response = self.client.patch(
            f"/api/questions/{self.question.id}/", {"text": "Moderated"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_moderator_cannot_use_moderate_action(self):
        self.client.force_authenticate(user=self.other)
        response = self.client.patch(
            f"/api/questions/{self.question.id}/moderate/", {"status": "resolved"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_moderator_can_use_moderate_action(self):
        moderator = User.objects.create_user(
            username="mod2", email="mod2@example.com", password="x", role=User.ROLE_MODERATOR,
        )
        self.client.force_authenticate(user=moderator)
        response = self.client.patch(
            f"/api/questions/{self.question.id}/moderate/", {"status": "resolved"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.question.refresh_from_db()
        self.assertEqual(self.question.status, Question.STATUS_RESOLVED)

    def test_anyone_can_read_questions(self):
        response = self.client.get("/api/questions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CommentActionTests(APITestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="chef", email="chef@example.com", password="x")
        self.topic = Topic.objects.create(name="Знаки", slug="signs")
        self.question = Question.objects.create(
            author=self.author, topic=self.topic, ticket_number=5, text="Вопрос",
        )

    def test_create_comment_requires_authentication(self):
        response = self.client.post(
            f"/api/questions/{self.question.id}/comments/", {"text": "Anon comment"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_comment(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.post(
            f"/api/questions/{self.question.id}/comments/", {"text": "Мой ответ"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.question.comments.count(), 1)
