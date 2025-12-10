from django.contrib import admin
from .models import Post, Category, Tag, Contact,Comment# Contact add karein

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'category', 'created_at', 'author') # Table mein yeh columns dikhenge
    list_filter = ('status', 'created_at', 'category', 'author') # Sidebar filter
    search_fields = ('title', 'content') # Search bar add ho jayega
    prepopulated_fields = {'slug': ('title',)} # Title likhte hi Slug khud ban jayega
    ordering = ('-created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}





# ... purana code ...

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')










from django.contrib import admin
from .models import Post, Category, Tag, Contact, Subscriber # <--- Subscriber import karein

# ... baaki code same rahega ...

# Neeche yeh naya block add karein
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)





@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)