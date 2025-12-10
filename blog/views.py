from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Post, Category
from django.db.models import Q
from .forms import ContactForm,SubscriberForm,CommentForm
from django.shortcuts import redirect
# 1. HOME & SEARCH VIEW
def index(request):
    # Saari published posts le aao
    posts = Post.published.all().select_related('category', 'author')
    
    # Search Logic Check
    query = request.GET.get('q') # Input ka name='q' hai
    if query:
        # Title YA Content mein dhundo
        posts = posts.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query)
        )

    context = {
        'posts': posts
    }

    # HTMX Check
    # Agar request HTMX se aayi hai, toh sirf partial template bhejo
    if request.headers.get('HX-Request'):
        return render(request, 'partials/blog_list.html', context)

    # Agar normal visit hai, toh full page bhejo
    return render(request, 'index.html', context)

# 2. POST DETAIL VIEW (With Related Posts)
def post_detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, status='published')
    
    # 1. Active comments fetch karein
    comments = post.comments.filter(active=True)
    new_comment = None
    
    # 2. Form Logic
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            # Reset form logic is handled by redirect usually, but here we just show success
            comment_form = CommentForm() # Clear form after submit
    else:
        comment_form = CommentForm()

    # 3. Related Posts logic (Purana wala)
    related_posts = Post.published.filter(category=post.category).exclude(id=post.id)[:3]

    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'related_posts': related_posts
    }
    return render(request, 'post_detail.html', context)

# 3. CATEGORY PAGE VIEW
def category_page(request, category_slug):
    # Category dhundo ya 404 error do
    category = get_object_or_404(Category, slug=category_slug)
    
    # Sirf us category ki posts laao
    posts = Post.published.filter(category=category).select_related('author')
    
    context = {
        'posts': posts,
        'category': category, 
    }
    
    # Hum same 'index.html' use kar rahe hain design ke liye
    return render(request, 'index.html', context)

# 4. ABOUT PAGE VIEW
def about(request):
    return render(request, 'about.html')

# 5. CONTACT VIEW
def contact(request):
    submitted = False
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save() # Database mein save karega
            submitted = True 
            form = ContactForm() # Reset form
    else:
        form = ContactForm()

    context = {
        'form': form,
        'submitted': submitted
    }
    return render(request, 'contact.html', context)











def subscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for subscribing!')
        else:
            messages.error(request, 'You are already subscribed or invalid email.')
            
    return redirect('home') # Wapas home par bhej do