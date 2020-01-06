from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

admin.site.register(Genre)
#admin.site.register(Author)
#admin.site.register(Book)
#admin.site.register(BookInstance)

class BookInline(admin.StackedInline):
    fields = ('title', 'summary')
    model = Book
    extra = 0

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ('first_name','last_name', ('date_of_birth','date_of_death'))
    inlines = [BookInline]

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 1

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    list_filter = ('title', 'author')
    fields = ('title', 'author', ('genre','isbn'))
    inlines = [BookInstanceInline]

class BookInstanceAdmin(admin.ModelAdmin):
    
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )


admin.site.register(Author, AuthorAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)

