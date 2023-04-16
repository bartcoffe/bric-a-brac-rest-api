from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Status(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'statuses'

    def __str__(self):
        return self.name


class Flashcard(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    code = models.CharField(max_length=2000)
    description = models.CharField(max_length=2000)
    hashtag = models.CharField(max_length=50)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    def __str__(self):
        return self.hashtag
