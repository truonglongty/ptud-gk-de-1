from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count
from .models import Post, Comment, UserProfile
from django.contrib import messages
from .forms import PostForm, CommentForm
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User

def home(request):
    posts = Post.objects.all().select_related('author').prefetch_related('comments')
    return render(request, 'blog/home.html', {'posts': posts})

def post_list(request):
    posts = Post.objects.all().select_related('author')
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(
                post=post,
                author=request.user,
                text=text
            )
            messages.success(request, 'Comment added successfully!')
        return redirect('post_detail', pk=post.pk)
    
    return render(request, 'blog/post_detail.html', {'post': post})

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def dashboard(request):
    user = request.user
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)

    user_posts = Post.objects.filter(author=user).count()
    user_comments = Comment.objects.filter(author=user).count()
    post_count = Post.objects.count()
    comment_count = Comment.objects.count()
    user_count = User.objects.count()
    actor_count = UserProfile.objects.filter(role='actor').count()
    recent_posts = Post.objects.order_by('-created_at')[:5]

    context = {
        'profile': profile,
        'user_posts': user_posts,
        'user_comments': user_comments,
        'post_count': post_count,
        'comment_count': comment_count,
        'user_count': user_count,
        'actor_count': actor_count,
        'recent_posts': recent_posts,
    }

    return render(request, 'blog/dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create UserProfile with default role 'user'
            UserProfile.objects.create(user=user, role='user')
            auth_login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

# Post CRUD Views
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Create'})

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("You don't have permission to edit this post.")
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'action': 'Update'})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("You don't have permission to delete this post.")
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

# Comment CRUD Views
@login_required
def comment_create(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('post_detail', pk=post_pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {
        'form': form, 
        'post': post,
        'action': 'Create'
    })

@login_required
def comment_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return HttpResponseForbidden("You don't have permission to edit this comment.")
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully!')
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment_form.html', {
        'form': form,
        'post': comment.post,
        'action': 'Update'
    })

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user:
        return HttpResponseForbidden("You don't have permission to delete this comment.")
    
    post_pk = comment.post.pk
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect('post_detail', pk=post_pk)
    return render(request, 'blog/comment_confirm_delete.html', {'comment': comment})
