import hashlib
import os
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=128)
    password_salt = models.CharField(max_length=32)

    date_of_birth = models.DateField(null=True, blank=True)

    date_of_birth = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username

    # ------------------------------------------------------------------
    # Birthday helpers
    # ------------------------------------------------------------------
    def is_birthday_today(self):
        if not self.date_of_birth:
            return False
        from datetime import date
        today = date.today()
        return (self.date_of_birth.month == today.month and
                self.date_of_birth.day == today.day)

    def age(self):
        if not self.date_of_birth:
            return None
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    # ------------------------------------------------------------------
    # Password handling
    # ------------------------------------------------------------------
    def set_password(self, raw_password):
        self.password_salt = os.urandom(16).hex()
        self.password_hash = self._hash(raw_password, self.password_salt)

    def check_password(self, raw_password):
        if not self.password_hash or not self.password_salt:
            return False
        return self.password_hash == self._hash(raw_password, self.password_salt)

    @staticmethod
    def _hash(raw_password, salt):
        return hashlib.sha256((salt + raw_password).encode()).hexdigest()

    # ------------------------------------------------------------------
    # Birthday helpers
    # ------------------------------------------------------------------
    def is_birthday_today(self):
        if not self.date_of_birth:
            return False
        from datetime import date
        today = date.today()
        return (self.date_of_birth.month == today.month and
                self.date_of_birth.day == today.day)

    def age(self):
        if not self.date_of_birth:
            return None
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )


class Bookmark(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookmarks',
    )
    meal_id = models.CharField(max_length=100)
    meal_name = models.CharField(max_length=255)
    meal_thumb = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'meal_id')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} bookmarked {self.meal_name}"
