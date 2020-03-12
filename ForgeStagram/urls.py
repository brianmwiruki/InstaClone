"""ForgeStagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import url, include
# from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from registration.backends.simple.views import RegistrationView
from insta.forms import RegisterForm
from django.contrib.auth import views

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'', include('insta.urls')),
    url(r'^accounts/register/$', RegistrationView.as_view(form_class=RegisterForm), name='register_to'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^logout/$', views.logout, {"next_page": '/'}), 
    url(r'^tinymce/', include('tinymce.urls')),


]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
