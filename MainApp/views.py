from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required




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
    elif request.method == "POST":
        # print("form data = ", list(request.POST.items()))
        # snippet = Snippet(
        #     name=request.POST["name"],
        #     lang=request.POST["lang"],
        #     code=request.POST["code"]
        # )
        # snippet.save()
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
        return redirect("snippets-list")


def snippets_page(request):
    # Извл. query параметр
    filter = request.GET.get('filter')
    snippets = Snippet.objects.all()
    pagename = 'Просмотр сниппетов'
    if filter:
        snippets = snippets.filter(user=request.user)
        pagename = 'Мои Сниппеты'
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
    context = {
        'pagename': pagename,
        'snippets': snippets,
        'lang': lang,
        'sort': sort
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


