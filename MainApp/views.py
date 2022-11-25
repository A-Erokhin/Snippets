from django.http import Http404
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from MainApp.models import Snippet
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from django.contrib.auth.models import User
from django.db.models import Count


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
        }
        return render(request, 'pages/add_snippet.html', context)
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
            # form.save()
            return redirect("snippets-list")
        return render(request, 'add_snippet.html', {'form':form})


def snippets_page(request):
    # Извл. query параметр
    filter = request.GET.get('filter')
    snippets = Snippet.objects.all()
    pagename = 'Просмотр сниппетов'
    users = User.objects.all().annotate(num_snippets=Count('snippet')).filter(num_snippets__gte=1)

    if filter:
        snippets = snippets.filter(user=request.user)
        pagename = 'Мои Сниппеты'

    username = request.GET.get('username')
    if username:
        filter_user = User.objects.get(username=username)
        snippets = snippets.filter(user=filter_user)

    lang = request.GET.get("lang")
    # print(f"{lang}")
    if lang is not None:
        snippets = snippets.filter(lang=lang)

    sort = request.GET.get("sort")
    if sort == 'name':
        snippets = snippets.order_by("name")
        sort = '-name'
    elif sort == '-name' or sort == 'init':
        snippets = snippets.order_by("-name")
        sort = 'name'
    if sort is None:
        sort = 'init'
    print(f"{sort}")
    sort2 = request.GET.get("sort2")
    if sort2 == 'lang':
        snippets = snippets.order_by("lang")
        sort2 = '-lang'
    elif sort2 == '-lang' or sort2 == 'init':
        snippets = snippets.order_by("-lang")
        sort2 = 'lang'
    if sort2 is None:
        sort2 = 'init'

    context = {
        'pagename': pagename,
        'snippets': snippets,
        'lang': lang,
        'sort': sort,
        'users': users,
    }
    return render(request, 'pages/view_snippets.html', context)

# def my_snippets_page(request):
#     snipps = Snippet.objects.filter(user=request.user)
#     context = {
#         'pagename': 'МОИ Сниппеты',
#         'snipps': snipps
#     }
#     return render(request, 'pages/view_snippets.html', context)

def snippet_detail(request, id):
    try:
        snipp = Snippet.objects.get(id=id)
    except ObjectDoesNotExist:
        raise Http404(f"Сниппет с id={id} не найден")
    comment_form = CommentForm()
    comments = snipp.comments.all()
    context = {
        "snipp": snipp,
        "comment_form": comment_form,
        "comments": comments,
    }
    return render(request, 'pages/snippet-detail.html', context)

# def create_snippet(request):
#     if request.method == "POST":
#         form = SnippetForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("redirect_url")
#         return render(request, 'add_snippet.html', {'form': form})

def login_page(request):
   if request.method == 'POST':
       username = request.POST.get("username")
       password = request.POST.get("password")
       # print("username =", username)
       # print("password =", password)
       user = auth.authenticate(request, username=username, password=password)
       if user is not None:
           auth.login(request, user)
       else:
           # Return error message
           pass
   return redirect(request.META.get('HTTP_REFERER', '/'))

def logout_page(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def registration(request):
    if request.method == "GET":
        form = UserRegistrationForm()
        context = {
            'form': form
        }
        return render(request, 'pages/registration.html', context)
    elif request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            context = {
                'form': form
            }
            return render(request, 'pages/registration.html', context)

def comment_add(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        snippet_id = request.POST["snippet_id"]
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = Snippet.objects.get(id=snippet_id)
            comment.save()
            return redirect("snippet-detail", snippet_id)
    raise Http404

@login_required
def snippet_delete(request, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
    if snippet.user != request:
        raise PermissionDenied
    snippet.delete()
    return redirect("view_snippets", snippet_id)

# def comments_list(request):

def users_rating(request):
    pagename = 'Рейтинг пользователей'
    users = User.objects.all()
    # for user in users:
    #     res = Snippet.objects.filter(user=user).Count
    context = {
        'pagename': pagename,
        'users': users,
    }
    return render(request, 'pages/user_rating.html', context)
