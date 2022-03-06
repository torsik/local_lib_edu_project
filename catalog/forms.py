from django import forms
from datetime import date
from .models import Book, Comment
from django.forms import ModelForm

class AuthorsForm(forms.Form):
    first_name = forms.CharField(label="Name")
    last_name = forms.CharField(label="Surname")
    date_of_birth = forms.DateField(label="Date of birth",
                                    initial=format(date.today()),
                                    widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    date_of_death = forms.DateField(label="Date of death",
                                    initial=format(date.today()),
                                    widget=forms.widgets.DateInput(attrs={'type': 'date'}))

class BookModelForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genre', 'language', 'author', 'summary', 'isbn']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
