from django.shortcuts import render
from .models import Post


def home(request):
    posts = Post.objects.select_related("author").order_by("-published_date")
    return render(request, "blog/home.html", {"posts": posts})

# Create your views here.
