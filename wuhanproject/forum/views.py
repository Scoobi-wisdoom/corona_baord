from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import *
from .forms import CreateBlogPostForm, UpdateBlogPostForm, CommentForm
from account.models import Account
from ipware import get_client_ip

BLOG_POSTS_PER_PAGE = 10


def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title'))
    return queryset


def post_list_view(request, *args, **kwargs):
    context = {}
    queryset = Post.objects.all()
    query = request.GET.get('q', '')
    # Search
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query)
        ).distinct()

    blog_posts = queryset.order_by('-date_published')

    # Pagination
    page = request.GET.get('page', 1)
    blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)
    try:
        blog_posts = blog_posts_paginator.page(page)
    except PageNotAnInteger:
        blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
    except EmptyPage:
        blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

    context['blog_posts'] = blog_posts
    context['query'] = query

    return render(request, "post_list.html", context)


def create_blog_view(request):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('account:must_authenticate')

    form = CreateBlogPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        author = Account.objects.filter(email=user.email).first()
        form.instance.author = author
        form.save()
        return redirect('forum:post_list')
        '''
        return redirect(reverse('blog:detail', kwargs={
            'id': form.instance.id,
            'title': form.instance.title
        }))
        '''

    context['form'] = form
    return render(request, "create_blog.html", context)


def detail_blog_view(request, title, id):
    blog_post = get_object_or_404(Post, id=id)
    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=blog_post)
    else:

        client_ip, is_routable = get_client_ip(request)
        if client_ip is None:
            pass
        # Unable to get the client's IP address
        else:
            PostViewIP.objects.get_or_create(ip=client_ip, post=blog_post)

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = request.user
            form.instance.post = blog_post
            form.save()
            return redirect(reverse("forum:detail", kwargs={
                'id': blog_post.id,
                'title': blog_post.title
            }))

    vote = False
    if request.user.is_authenticated:
        vote = PostUp.objects.filter(user=request.user, post=blog_post).exists()

    context = {
        'blog_post': blog_post,
        'form': form,
        'vote': vote
    }

    if blog_post.title != title:\
        return redirect(reverse("forum:detail", kwargs={
            'id': blog_post.id,
            'title': blog_post.title
        }))
    return render(request, 'detail_blog.html', context)


def edit_blog_view(request, title, id):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect('account:must_authenticate')

    blog_post = get_object_or_404(Post, title=title, id=id)

    if blog_post.author != user:
        return HttpResponse('You are not the author of that post.')

    if request.POST:
        form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Updated"
            blog_post = obj
            return redirect('forum:post_list')

    form = UpdateBlogPostForm(
        initial={
            "title": blog_post.title,
            "body": blog_post.body,
        }
    )

    context['form'] = form
    context['error'] = "Something wrong, max length is 5000"

    return render(request, 'edit_blog.html', context)


def delete_blog_view(request, title, id):
    user = request.user
    blog_post = get_object_or_404(Post, title=title, id=id)

    if blog_post.author != user:
        return HttpResponse('You are not the author of that post.')

    if request.POST:
        blog_post.delete()
        return redirect('forum:post_list')
    return render(request, 'delete_blog.html')


def delete_comment_view(request, title, id, cid):
    user = request.user
    blog_post = get_object_or_404(Post, title=title, id=id)
    comment = Comment.objects.get(post=blog_post, id=cid)

    if comment.author != user:
        return HttpResponse('You are not the author of that comment.')

    if request.POST:
        comment.delete()
        return redirect('../../')
    return render(request, 'delete_comment.html')


@ensure_csrf_cookie
def up_vote_view(request, id, title):
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.is_ajax():
                post = None
                try:
                    post = Post.objects.get(id=id)
                except Exception as e:
                    print(e)
                    return JsonResponse({'res': 0})
                post_up, created = PostUp.objects.get_or_create(post=post, user=request.user)
                liked = 'true'
                if not created:
                    post_up.delete()
                    liked = 'false'
                return JsonResponse({'res': 1, 'up': liked})
        return JsonResponse({'res': 2})


'''
def get_blog_queryset(query=None):
    queryset = []
    queries = query.split(" ") # python install 2019 = [python, install, 2019]
    for q in queries:
        posts = Post.objects.filter(
                Q(title__icontains=q) |
                Q(body__icontains=q)
            ).distinct()

        for post in posts:
            queryset.append(post)

    return list(set(queryset))
'''
