"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView

from django.contrib.sitemaps.views import sitemap
from notes.sitemaps import PostSitemap
from django.conf.urls.i18n import i18n_patterns
sitemaps = {'posts': PostSitemap,}

urlpatterns = (
    [
        path("login", auth_views.LoginView.as_view(), name="login"),
        path("logout", auth_views.LogoutView.as_view(), name="logout"),

        path('notes/comments/', include('django_comments.urls')),
        path('notes/', include('notes.urls', namespace = 'notes')),
        path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
        path('ckeditor/', include('ckeditor_uploader.urls')),
        path('search/', include('haystack.urls')),
        
        path('uploads/', include('uploads.urls', namespace = 'uploads')),
        path("todo/", include("todo.urls", namespace="todo")),
        path('calendar/', include('cal.urls', namespace="calendar")),
        path('admin/', admin.site.urls),
        path('', TemplateView.as_view(template_name="home.html"), name="home"),
    ]
    # Static media in DEBUG mode:
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
