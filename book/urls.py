"""book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url, include

from django.contrib import admin
from django.urls import path
from app01 import views
from app01 import views
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.static import serve
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('publish/', views.publish_list),
    path('publish_add/', views.Publisher_add.as_view()),
    path('publish_del/', views.publish_del),
    path('publish_edit/', views.publish_edit),
    path('book/', views.book_list),
    path('book_del/', views.book_del),
    path('book_edit/', views.book_edit),
    path('book_pic/', views.book_pic),
    path('book_add/', views.book_add),
    path('author/', views.author),
    path('author_add/', views.author_add),
    path('author_del/', views.author_del),
    path('author_edit/', views.author_edit),
    path('detail/<int:pk>/', views.VideoDetailView.as_view(), name='detail'),
    path('mom/', views.mom),
    path('video_add/', views.AddVideoView.as_view(), name='video_add'),
    path('chunked_upload/', views.MyChunkedUploadView.as_view(), name='api_chunked_upload'),
    path('chunked_upload_complete/', views.MyChunkedUploadCompleteView.as_view(), name='api_chunked_upload_complete'),
    path('video_publish/<int:pk>/', views.VideoPublishView.as_view(), name='video_publish'),
    path('video_publish_success/', views.VideoPublishSuccessView.as_view(), name='video_publish_success'),
    path('video_list/', views.VideoListView.as_view(), name='video_list'),
    path('', views.IndexView.as_view(), name='index'),
    path('author_del2/', views.author_del2),
    path('index/', views.index),
    # path('media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})#命名分组，变成关键字传参
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


