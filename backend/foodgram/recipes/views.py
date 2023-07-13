from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Follow, Ingredient, Recipe, Tag
from .utils import paginatored

User = get_user_model()


def index(request):
    recipes = Recipe.objects.select_related('title', 'author')
    page_obj = paginatored(recipes, settings.AMAUNT_POST_ON_PAGE, request)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'recipes/index.html', context)


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    comments = recipe.comments.all()
    form = CommentForm()
    context = {
        'recipe': recipe,
        'comments': comments,
        'form': form
    }
    return render(request, 'recipe/recipe_detail.html', context)


def user_profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.recipes.select_related('title', 'author')
    page_obj = paginatored(posts, settings.AMAUNT_POST_ON_PAGE, request)
    following = (
        request.user.is_authenticated
        and author.following.filter(user=request.user).exists()
    )
    context = {
        'page_obj': page_obj,
        'author': author,
        'following': following
    }
    return render(request, 'posts/profile.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None, request.FILES)
    if form.is_valid():
        create_post = form.save(commit=False)
        create_post.author = request.user
        create_post.save()
        return redirect('posts:profile', create_post.author)
    context = {
        'form': form
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, recipes_id):
    edit_post = get_object_or_404(Recipe, id=recipes_id)
    if request.user != edit_post.author:
        return redirect('posts:post_detail', recipes_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=edit_post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', recipes_id)
    context = {
        'form': form,
        'is_edit': True,
        'post': edit_post
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def add_comment(request, recipes_id):
    post = get_object_or_404(Recipe, id=recipes_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=recipes_id)


@login_required
def follow_index(request):
    posts = Recipe.objects.filter(
        author__following__user=request.user)
    page_obj = paginatored(posts, settings.AMAUNT_POST_ON_PAGE, request)
    context = {'page_obj': page_obj}
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('posts:profile', author)


@login_required
def profile_unfollow(request, username):
    user_follower = get_object_or_404(
        Follow,
        user=request.user,
        author__username=username
    )
    user_follower.delete()
    return redirect('posts:profile', username)


def page_not_found(request, exception):
    """Ошибка 404 - страница не найдена"""
    return render(request, 'core/404.html', {'path': request.path}, status=404)
