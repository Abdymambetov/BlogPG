# from django.shortcuts import HttpResponse, redirect
from django.shortcuts import render, redirect
from posts.models import Post, Hashtag, Comment
from posts.forms import PostCreateForm, CommentCreateForm
# import reder

# Create your views here.

def main_view(request):
    return render(request, 'layouts/index.html')
    # return HttpResponse('Hello! It is my first view!')

def posts_view(request):
    # b = []
    # a=[b]
    # b=[b]
    # print(a is b)
    if request.method == 'GET':
        hashtag_id = int(request.GET.get('hashtag_id', 0))

        if hashtag_id:
            posts = Post.objects.filter(hashtags__in=[hashtag_id])
        else: 
            posts = Post.objects.all()

        return render(request, 'posts/posts.html', context={
            'posts': posts
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
        form = PostCreateForm(data=request.POST)

        if form.is_valid():
            Post.objects.create(
                # title=request.POST.get('title'),
                # description=request.POST.get('description'),
                # rate=request.POST.get('rate', 0)
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
