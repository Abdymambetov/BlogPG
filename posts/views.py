# from django.shortcuts import HttpResponse, redirect
from typing import Any
from django.shortcuts import render, redirect
from posts.models import Post, Hashtag, Comment
from posts.forms import PostCreateForm, CommentCreateForm
from django.views.generic import ListView, CreateView, DetailView


# Create your views here.


PAGINATION_LIMIT = 3

def main_view(request):
    return render(request, 'layouts/index.html')
    # return HttpResponse('Hello! It is my first view!')



class PostsCBV(ListView):
    model = Post
    template_name = 'posts/posts.html'
    context_object_name = 'posts'


    def get_context_data(self, *, object_list=None, **kwars):
        return {
            'posts': kwars['posts'],
            'pages': kwars['max_page'],
            'user': kwars['user']
        }

    def get(self, request, **kwargs):
        hashtag_id = int(request.GET.get('hashtag_id', 0))
        text = request.GET.get('text')
        page = int(request.GET.get('page', 1))


        if hashtag_id:
            posts = self.model.objects.filter(hashtags__in=[hashtag_id])
        else: 
            posts =self.model.objects.all()

        if text:
            posts = self.model.objects.filter(title__contains=text)

        max_page = posts.__len__() / PAGINATION_LIMIT
        print(max_page)
        if round(max_page) <= max_page: 
            max_page = round(max_page)+1

        max_page = int(max_page)
        print(max_page)
        posts = posts[PAGINATION_LIMIT * (page-1):PAGINATION_LIMIT * page]

        return render(
            request, 
            self.template_name, 
            context=self.get_context_data(
                posts=posts,
                user=None if request.user.is_anonymous else request.user,
                max_page=range(1, max_page+1)
            )
        )



def posts_view(request):
    # b = []
    # a=[b]
    # b=[b]
    # print(a is b)
    if request.method == 'GET':
        hashtag_id = int(request.GET.get('hashtag_id', 0))
        text = request.GET.get('text')
        page = int(request.GET.get('page', 1))


        if hashtag_id:
            posts = Post.objects.filter(hashtags__in=[hashtag_id])
        else: 
            posts = Post.objects.all()

        if text:
            posts = Post.objects.filter(title__contains=text)

        max_page = posts.__len__() / PAGINATION_LIMIT
        print(max_page)
        if round(max_page) <= max_page: 
            max_page = round(max_page)+1

        max_page = int(max_page)
        print(max_page)
        posts = posts[PAGINATION_LIMIT * (page-1):PAGINATION_LIMIT * page]

        return render(request, 'posts/posts.html', context={
            'posts': posts,
            'user': None if request.user.is_anonymous else request.user,
            'pages': range(1, max_page+1)
        })



def post_detail_view(request, id):
    if request.method == 'GET':
        post = Post.objects.get(id=id)
        comments = post.comment_set.all()
        hashtags = post.hashtags.all()
        print(comments)
        context = {
            'post': post,
            'comments': comments,
            'hashtags': hashtags,
            'comment_form': CommentCreateForm
        }
        return render(request, 'posts/detail.html', context=context)
    
    if request.method == 'POST':
        post = Post.objects.get(id=id)
        form = CommentCreateForm(data=request.POST)

        if form.is_valid():
            Comment.objects.create(
                author = request.user,
                post_id=id,
                text=form.cleaned_data.get('text')
            )
            return redirect(f'/posts/{id}/')
        else: 
            return render(request, 'posts/detail.html', context={
            'post': post,
            'comments': comments,
            'hashtags': hashtags,
            'comment_form': form
        })




def hashtags_view(request):
    if request.method=='GET':
        hashtags = Hashtag.objects.all()

        context = {
            'hashtags': hashtags
        }
        return render(request, 'hashtags/index.html', context=context)
    



def post_create_view(request):
    if request.method == 'GET':
        return render(request, 'posts/create.html', context={
            'form': PostCreateForm
        })
    
    if request.method == 'POST':
        # form = PostCreateForm(data=request.POST)
        form = PostCreateForm(request.POST, request.FILES)
        print(form.is_valid(), request.FILES)

        if form.is_valid():
            Post.objects.create(
                # title=request.POST.get('title'),
                # description=request.POST.get('description'),
                # rate=request.POST.get('rate', 0)
                image = form.cleaned_data.get('image'),
                author = request.user,
                title = form.cleaned_data.get('title'),
                description = form.cleaned_data.get('description'),
                rate = form.cleaned_data.get('rate', 0)
            )
            return redirect('/posts/')
        else:
            return render(request, 'posts/create.html', context={
                'form': form
            })
        # errors = {}
        # if len(request.POST.get('title')) < 8:
        #     errors['title_error'] = 'min length in field title 8!'
        # if len(request.POST.get('description')) < 1:
        #     errors['description_error'] = 'this fiels is required!'
        # if len(errors.keys()) > 0:
        #     return render(request, 'posts/create.html', context=errors)
        





# def google_redirect_view(request):
#     return redirect('https://google.com')
#
# def youtube_redurect_view(request):
#     return redirect('https://youtube.com')
