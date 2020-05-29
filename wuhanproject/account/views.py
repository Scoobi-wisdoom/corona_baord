from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from .forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from forum.models import Post


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # email = form.cleaned_data.get('email')
            # raw_password = form.cleaned_data.get('password1')
            account = form.save()
            # account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('forum:post_list')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'register.html', context)


def logout_view(request):
    logout(request)
    return redirect('forum:post_list')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("forum:post_list")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("forum:post_list")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    # print(form)
    return render(request, "login.html", context)


def account_view(request):
    if not request.user.is_authenticated:
        return redirect("account:login")

    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST['email'],
                "username": request.POST['username'],
            }
            form.save()
            context['success_message'] = "Updated"
    else:
        form = AccountUpdateForm(

            initial={
                "email": request.user.email,
                "username": request.user.username,
            }
        )

    context['account_form'] = form

    blog_posts = Post.objects.filter(author=request.user)
    context['blog_posts'] = blog_posts

    return render(request, "account.html", context)


def must_authenticate_view(request):
    return render(request, 'must_authenticate.html', {})
