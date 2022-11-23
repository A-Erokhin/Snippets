from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('snippets/add', views.add_snippet_page, name='add-snippet'),
    path('snippets/list', views.snippets_page, name='snippets-list'),
    path('snippets/<int:id>',views.snippet_detail, name='snippet-detail'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_page, name='logout'),
    path('registration', views.registration, name='registration'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


