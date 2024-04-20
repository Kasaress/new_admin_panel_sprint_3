import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True,)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.TextField(_('full_name'))

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    def __str__(self):
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedMixin):
    class TypeChoices(models.TextChoices):
        MOVIE = _('movie'), _('Movie')
        TV_SHOW = _('tv_show'), _('TV Show')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True,)
    creation_date = models.DateField(
        _('creation_date'), blank=True, null=True,
    )
    rating = models.FloatField(_('rating'), blank=True, null=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    type = models.TextField(_('type'), choices=TypeChoices.choices)
    genres = models.ManyToManyField(
        Genre, through='GenreFilmwork', verbose_name=_('genres')
    )
    persons = models.ManyToManyField(
        Person, through='PersonFilmwork', verbose_name=_('persons')
    )

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('movie')
        verbose_name_plural = _('movies')
        indexes = [
            models.Index(
                fields=['creation_date', 'rating'],
                name='film_work_creation_rating_idx'
            ),
        ]

    def __str__(self):
        return self.title


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        'Filmwork', on_delete=models.CASCADE, verbose_name=_('movie')
    )
    genre = models.ForeignKey(
        'Genre', on_delete=models.CASCADE, verbose_name=_('genre')
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('genre_film_work')
        verbose_name_plural = _('genre_film_works')
        indexes = [
            models.Index(
                fields=['film_work_id', 'genre_id'],
                name='film_work_genre_idx'
            ),
        ]

    def __str__(self):
        return f'Жанры кинопроизведения {self.film_work.title}'


class PersonFilmwork(UUIDMixin):
    class TypeChoices(models.TextChoices):
        ACTOR = _('actor'), _('Actor')
        WRITER = _('writer'), _('Writer')
        DIRECTOR = _('director'), _('Director')

    film_work = models.ForeignKey(
        'Filmwork', on_delete=models.CASCADE, verbose_name=_('movie')
    )
    person = models.ForeignKey(
        'Person', on_delete=models.CASCADE, verbose_name=_('person')
    )
    role = models.TextField(_('role'), choices=TypeChoices.choices)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('person_film_work')
        verbose_name_plural = _('person_film_works')
        indexes = [
            models.Index(
                fields=['film_work_id', 'person_id', 'role'],
                name='film_work_person_idx'
            ),
        ]

    def __str__(self):
        return f'Персоны кинопроизведения {self.film_work.title}'
