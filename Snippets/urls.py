from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views
from django.contrib import admin


urlpatterns = [
    path('', views.index_page, name='home'),
    path('snippets/add', views.add_snippet_page, name='add-snippet'),
    path('snippets/list?filter=my?lang=py', views.snippets_page, name='snippets-list'),
    # path('snippets/my', views.snippets_page, {'my':True}, name='snippets-my'),
    path('snippets/<int:id>',views.snippet_detail, name='snippet-detail'),
    path('snippets/<int:id>/delete',views.snippet_delete, name='snippet-delete'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_page, name='logout'),
    path('registration', views.registration, name='registration'),
    path('comment/add', views.comment_add, name="comment_add"),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


