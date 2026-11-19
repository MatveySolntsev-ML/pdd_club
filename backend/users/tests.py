from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username="vasya", email="vasya@example.com", password="x",
        )
        self.assertEqual(user.role, User.ROLE_USER)
        self.assertFalse(user.is_moderator)

    def test_email_must_be_unique(self):
        User.objects.create_user(username="vasya", email="dup@example.com", password="x")
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username="petya", email="dup@example.com", password="x")

    def test_is_moderator_property(self):
        mod = User.objects.create_user(
            username="mod", email="mod@example.com", password="x", role=User.ROLE_MODERATOR,
        )
        self.assertTrue(mod.is_moderator)


class UserRegistrationAPITests(APITestCase):
    def test_register_and_login(self):
        response = self.client.post(
            "/api/users/",
            {"username": "vasya", "email": "vasya@example.com", "password": "Qwerty123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", response.data)

        login = self.client.post(
            "/api/auth/token/",
            {"username": "vasya", "password": "Qwerty123"},
            format="json",
        )
        self.assertEqual(login.status_code, status.HTTP_200_OK)
        self.assertIn("access", login.data)


class SubscribeActionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="follower", email="f@example.com", password="x")
        self.author = User.objects.create_user(username="author", email="a@example.com", password="x")
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        response = self.client.post(f"/api/users/{self.author.id}/subscribe/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_subscribe_to_self(self):
        response = self.client.post(f"/api/users/{self.user.id}/subscribe/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_subscribe_twice(self):
        self.client.post(f"/api/users/{self.author.id}/subscribe/")
        response = self.client.post(f"/api/users/{self.author.id}/subscribe/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsubscribe(self):
        self.client.post(f"/api/users/{self.author.id}/subscribe/")
        response = self.client.delete(f"/api/users/{self.author.id}/subscribe/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_subscribe_requires_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(f"/api/users/{self.author.id}/subscribe/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
