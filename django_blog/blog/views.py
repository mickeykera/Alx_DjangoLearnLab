from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import RegistrationForm, ProfileForm


def home(request):
    posts = Post.objects.select_related("author").order_by("-published_date")
    return render(request, "blog/home.html", {"posts": posts})


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "registration/profile.html", {"form": form})

# Create your views here.
