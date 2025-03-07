from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Category, Post, Comment
from django.contrib.auth.models import User
from .forms import  CreatePostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden
from taggit.models import Tag
from django.db.models import Count

def index(request):
    """
    Presentation a main page of the list posts

    Posts are available when post status is published
    Posts split into pages using Paginator

    Context:
        categories: list of categories
        page_obj: page object with the list posts for current page
        status: selected post status from the request
        posts: queryset of all posts
    
    Template:
        - index.html
    """
    status = request.GET.get('status', 'published')
    posts = Post.objects.filter(status=status).order_by('-created_at')

    categories = Category.objects.all()

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'page_obj': page_obj, 
        'status':status, 
        'posts':posts
    }
    return render(request, 'index.html', context)

@login_required
def detail_post(request, slug):
    """
    Presentation detail information about the product.

    Get a post by slug from database and increment the number of views
    Ability to leave a comment on the post. After saving comment, user is redirected to detail_post view

    Context:
        - post: detail information about post
        - comments: queryset of all products for the product
        - comment_form: form for adding comment
    
    Template:
        - detail_post.html
    """

    post = get_object_or_404(Post, slug = slug)
    post.views += 1
    post.save()

    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment_form.save()
            return redirect('detail_post', slug=post.slug)
    else:
        comment_form = CommentForm()

    context = {
        'post':post,
        'comments':comments,
        'comment_form': comment_form
    }
    return render(request, 'detail_post.html', context)


def post_by_category(request, slug):
    """
    Presentation of the posts by category.

    Get a category by slug from database and filter products by this category.
    Split into pages using Paginator.

    Context:
        - category: detail information about category.
        - posts: queryset of all products in this category.
        - page_obj: page object with the list of posts for the current page.
        - categories: queryset of all categoies
    
    Templates:
        - product_by_category.html"
    """


    category = get_object_or_404(Category, slug = slug)

    posts = Post.objects.filter(category = category)

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'posts':posts,
        'categories':categories,
        'page_obj':page_obj,
        'category':category
    }

    return render(request, 'post_by_category.html', context)


def post_by_author(request, username):
    """
    Presentation of the posts by author.

    Get author by username from database and filter products by this author.
    Split into pages using Paginator.

    Context:
        - author: get auhtor by username.
        - posts: queryset of all products in this category.
        - page_obj: page object with the list of posts for the current page.
    
    Templates:
        - product_by_author.html"
    """
    author = get_object_or_404(User, username = username)

    posts = Post.objects.filter(author = author)

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'author':author,
        'posts':posts,
        'page_obj':page_obj,
    }

    return render(request, 'post_by_author.html', context)

@staff_member_required
@login_required
def create_post(request): 
    """
    Presentation view for creation of a new post.

    This view allows authenticated staff members to create a new post.  
    If the request method is POST and the form is valid, the post is saved with  
    the current user as the author
    After saving, the user is redirected to the index page.  

    Context:
        - form: form for creating a new posts

    Template:
        - create_post.html
    """
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('index')
    else:
        form = CreatePostForm()

    context = {
        'form':form
    }

    return render(request, 'create_post.html', context)

@login_required
@staff_member_required
def edit_post(request, slug):
    """
    Presentation view editing an existing post.

    This view allows authenticated staff members to edit their own posts.  
    The post is retrieved using the provided slug.  
    If the request method is POST and the user is the author, the form is validated and saved.  
    The user is then redirected to their posts page.  

    Context:
        - form: form for editing posts
    """
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST' and post.author == request.user:
        form = CreatePostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_by_author', username=request.user.username)
    else:
        form = CreatePostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form})
 
@login_required
@staff_member_required
def delete_post(request, pk):
    """
    Handle deleting a post.

    This view allows staff members to delete a post.  
    The post is retrieved using its primary key.  
    If the current user is not the post's author and is not a staff member,  
    an HTTP 403 Forbidden response is returned.  
    Otherwise, the post is deleted, and the user is redirected to their posts page

    """
    post = get_object_or_404(Post, pk = pk)

    if post.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden("Ви не маєте права видаляти цей пост.")
    
    post.delete()
    return redirect('post_by_author', username=request.user.username)