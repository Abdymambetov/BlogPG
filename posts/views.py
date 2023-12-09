from django.shortcuts import HttpResponse, redirect

# Create your views here.

def main_view(request):
    return HttpResponse('Hello! It is my first view!')

def google_redirect_view(request):
    return redirect('https://google.com')

def youtube_redurect_view(request):
    return redirect('https://youtube.com')
