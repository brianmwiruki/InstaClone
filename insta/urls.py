from django.urls import path, include
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    PostListView,
    PostCreateView,
    PostDetailView,
)

app_name = 'insta'

urlpatterns = [
    # path('', PostListView.as_view(),name= 'post_list'),
    # path('new/', PostCreateView.as_view(), name= 'post_create'),
    # path('<int:id>', PostDetailView.as_view(), name='post_detail')
    url(r'^$', views.home, name= 'home'),
    url(r'^search/', views.search_images, name='search_results'),
    url(r'^image/(\d+)', views.get_image, name='image_results'),
    url(r'^new/image$', views.new_image, name='new-image'),
    url(r'^accounts/profile/$', views.user_profiles, name='profile'),
    url(r'^like/(\d+)', views.like_image, name='like_image'),

]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)