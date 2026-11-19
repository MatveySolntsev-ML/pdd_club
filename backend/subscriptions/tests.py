from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from subscriptions.models import Subscription

User = get_user_model()


class SubscriptionModelTests(TestCase):
    def setUp(self):
        self.follower = User.objects.create_user(username="follower", email="f@example.com", password="x")
        self.author = User.objects.create_user(username="author", email="a@example.com", password="x")

    def test_create_subscription(self):
        sub = Subscription.objects.create(follower=self.follower, author=self.author)
        self.assertEqual(sub.follower, self.follower)

    def test_duplicate_subscription_rejected(self):
        Subscription.objects.create(follower=self.follower, author=self.author)
        with self.assertRaises(IntegrityError):
            Subscription.objects.create(follower=self.follower, author=self.author)

    def test_self_subscription_rejected_by_db_constraint(self):
        with self.assertRaises(IntegrityError):
            Subscription.objects.create(follower=self.follower, author=self.follower)
