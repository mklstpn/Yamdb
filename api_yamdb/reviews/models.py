from api.validators import year_validator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint
from users.models import User


class Category(models.Model):
    name = models.CharField("Категория", max_length=50)
    slug = models.SlugField(unique=True, default="", db_index=True)


class Genre(models.Model):
    name = models.CharField("Жанр", max_length=256)
    slug = models.SlugField(unique=True, default="")


class Title(models.Model):
    name = models.CharField("Произведение", max_length=50)
    year = models.IntegerField(validators=[year_validator],
                               null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 blank=True, null=True)
    genre = models.ManyToManyField(Genre)
    description = models.TextField(blank=True, null=True, max_length=100)

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews', blank=True, null=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    score = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['pub_date']
        constraints = [
            CheckConstraint(check=Q(score__range=(0, 10)), name='valid_score'),
            UniqueConstraint(fields=['author', 'title'], name='rating_once'),
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments', null=True)
    text = models.TextField()
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления', auto_now_add=True, db_index=True)
