from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone


# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=40, help_text="Insert genre", verbose_name="Genre")

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=30, help_text="Type the language",
                            verbose_name="Book languauge")

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=40,
                                  help_text="Type name",
                                  verbose_name="Author's name")
    last_name = models.CharField(max_length=30,
                                 help_text="Type surname",
                                 verbose_name="Author's surname")
    date_of_birth = models.DateField(help_text="Type date of birth",
                                     verbose_name="Date of birth",
                                     null=True, blank=True)
    date_of_death = models.DateField(help_text="Type date of death",
                                     verbose_name="Date of death",
                                     null=True, blank=True)

    def __str__(self):
        return self.last_name


class Book(models.Model):
    title = models.CharField(max_length=100, help_text="Type title of the book",
                             verbose_name="Title of the book")
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE,
                              help_text="Genre of the book",
                              verbose_name="Genre", null=True)
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 help_text="Choose the language",
                                 verbose_name="Language", null=True)
    author = models.ManyToManyField('Author', help_text="Choose the author",
                                    verbose_name="Author of the book", null=True)
    summary = models.CharField(max_length=1000, help_text="Brief summary",
                               verbose_name="Annotation")
    isbn = models.CharField(max_length=13, help_text="Should contain 13 charaters",
                            verbose_name="ISBN book")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_author(self):
        return ', '.join([author.last_name for author in self.author.all()])

    display_author.short_description = 'Authors'  # to display AUTHORS is admin


class BookInstance(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)
    inv_nom = models.CharField(max_length=20, null=True,
                               help_text="Type inventar nomer",
                               verbose_name='Inventar nomer')
    imprint = models.CharField(max_length=50, help_text='Publisher and year',
                               verbose_name='Publisher')
    BOOK_STAT = (
        ('a', 'available'),
        ('r', 'reserved'),
        ('s', 'sold'),
    )
    status = models.CharField(max_length=1, choices=BOOK_STAT, null=True,
                              help_text='Book availability',
                              verbose_name='Status')
    # default = 'a'???

    due_back = models.DateField(null=True, blank=True,
                                help_text='Input the end of the period',
                                verbose_name='End date of the status')

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 verbose_name='Customer',
                                 help_text='Choose customer for the book')

    def __str__(self):
        return '%s %s %s' % (self.inv_nom, self.book, self.status)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

class NewsPost(models.Model):
    STATUS_NEWS = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=70)
    slug = models.SlugField(max_length=100, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_NEWS, default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    '''def get_absolute_url(self):
        return reverse('newspost_detail', args=[str(self.id)])'''

    def get_absolute_url(self):
        return reverse('news_detail', args=[self.publish.year, self.publish.month,
                                            self.publish.day, self.slug])

class Comment(models.Model):
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=30)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)