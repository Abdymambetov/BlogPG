# from django.shortcuts import HttpResponse, redirect
from django.shortcuts import render
from posts.models import Post
# import reder

# Create your views here.

def main_view(request):
    return render(request, 'layouts/index.html')
    # return HttpResponse('Hello! It is my first view!')

def posts_view(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        return render(request, 'posts/posts.html', context={
            'posts': posts
        })

# def google_redirect_view(request):
#     return redirect('https://google.com')
#
# def youtube_redurect_view(request):
#     return redirect('https://youtube.com')
