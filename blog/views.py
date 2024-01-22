from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import NewPostForm, EditPostForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    posts = Post.objects.all()
    return render(request, "blog/index.html",{
        "posts": posts,
    })


@login_required(login_url="authuser:login")
def compose(request):
    form = NewPostForm()

    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Your post has been posted successfully")

            return redirect("blog:index")

    return render(request, "blog/form.html",{
        "form": form,
        "title": "compose blog",
    })


@login_required
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    related_posts = Post.objects.filter(author=post.author).exclude(pk=pk)
    return render(request, "blog/detail.html", {
        "post": post,
        "related_posts": related_posts,
    })


@login_required(login_url="authuser:login")
def edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    form = EditPostForm(instance=post)

    if request.method == "POST":
        form = EditPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Your post has been edited successfully")
            return redirect("blog:detail", pk=pk)

    return render(request, "blog/form.html", {
        "form": form,
        "title": "Edit post"
    })


@login_required(login_url="authuser:login")
def delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        post.delete()
        messages.info(request, f"{post.title} has been deleted.")
        return redirect("blog/index")

    return render(request, "blog/delete.html", {
        "post": post,
    })


def dashboard(request):
    post = Post.objects.filter(author=request.user)
    context = {
        'post': post
    }
    return render(request, "blog/dashboard.html", context)


