from django.shortcuts import render, get_object_or_404
from django.http import *
from .models import Book, BookInstance, Genre, Author, NewsPost, Comment
from django.views import generic #for work with LISTVIEW
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AuthorsForm, CommentForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from taggit.models import Tag
from django.core.paginator import  Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(request, 'index.html',
                  context={'num_books': num_books,
                           'num_instances': num_instances,
                           'num_authors': num_authors,
                           'num_instance_available': num_instances_available,
                           'num_visits': num_visits})

class BookListView(generic.ListView):
    model = Book
    paginate_by = 5

class BookDetailView(generic.DetailView):
    model = Book

class AuthorsListView(generic.ListView):
    model = Author
    paginate_by = 5

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 5

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status='r').order_by('due_back')

def authors_add(request):
    author = Author.objects.all()
    authorsform = AuthorsForm()
    return render(request, "catalog/authors_add.html",
                  {"form": authorsform, "author": author})

def create_author(request):
    if request.method == "POST":
        author = Author()
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get("last_name")
        author.date_of_birth = request.POST.get("date_of_birth")
        author.date_of_death = request.POST.get("date_od_death")
        author.save()
        return HttpResponseRedirect("/authors_add")

def delete_author(request, id):
    try:
        author = Author.objects.get(id=id)
        author.delete()
        return HttpResponseRedirect("/authors_add")
    except Author.DoesNotExist:
        return HttpResponseNotFound("<h2>Author is not found</h2>")

def edit_author(request, id):
    author = Author.objects.get(id=id)
    if request.method == "POST":
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get("last_name")
        author.date_of_birth = request.POST.get("date_of_birth")
        author.date_of_death = request.POST.get("date_od_death")
        author.save()
        return HttpResponseRedirect("/authors_add")
    else:
        return render(request, "catalog/edit_author.html", {"author": author})

class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')

'''class NewsPostListView(generic.ListView):
    model = NewsPost
    paginate_by = 5'''


def news_list(request):
    posts = NewsPost.objects.all()
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'catalog/newspost_list.html', {'page': page, 'posts': posts})

def news_detail(request, year, month, day, newspost):
    newspost = get_object_or_404(NewsPost, slug=newspost, status='published',
                                publish__year=year, publish__month=month, publish__day=day)
    comments = newspost.comments.filter(active=True)
    new_comment = None
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = newspost
            new_comment.save()
        else:
            comment_form = CommentForm()
    return render(request, 'catalog/news_detail.html', {'newspost': newspost,
                                                        'comments': comments,
                                                        'new_comment': new_comment,
                                                        'comment_form': comment_form})


