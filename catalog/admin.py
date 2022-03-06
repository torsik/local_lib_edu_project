from django.contrib import admin
from .models import Author, Book, Genre, Language, BookInstance, NewsPost, Comment

# Register your models here.

#admin.site.register(Author)
class AuthorAdmin(admin.ModelAdmin): #MDDELADMIN for displaying elements in adminka
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

admin.site.register(Author, AuthorAdmin)

class BookInstanceInline(admin.TabularInline): # add bookinstance to book tab
    model = BookInstance

#admin.site.register(Book)
@admin.register(Book) # register admin class for books
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'language', 'display_author') #display_authors for join tables
    list_filter = ('genre', 'author', 'language')
    inlines = [BookInstanceInline]

admin.site.register(Genre)
admin.site.register(Language)

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('book', 'status')
    list_display = ('book', 'inv_nom', 'status', 'borrower', 'due_back')
    fieldsets = (
        ('Instance', {
            'fields': ('book', 'imprint', 'inv_nom')
        }),
        ('Status and End date of the status', {
            'fields': ('status', 'due_back', 'borrower')
        })
    )
#admin.site.register(BookInstance)
#admin.site.register()
#admin.site.register()

@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_filter = ('title', 'author')
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    search_fields = ('title', 'body')
    date_hierarchy = 'publish'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')