"""
URL configuration for blogAssignment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import blogAssignment.services.blog_view as blog_views
import blogAssignment.services.comment_view as comment_views
import blogAssignment.services.account_view as user_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register/', user_views.register),
    path('blogs/create/', blog_views.create_blog),
    path('blogs/<int:blog_id>/update/', blog_views.update_blog),
    path('blogs/<int:blog_id>/increment-view/', blog_views.increment_view_count),
    path('blogs/<int:blog_id>/toggle_blog_status/', blog_views.toggle_blog_status),
    path('blogs/', blog_views.get_blogs),
    path('blogs/all/', blog_views.get_all_blogs),
    path('blogs/<int:blog_id>/', blog_views.get_blog_detail),
    path('blogs/<int:blog_id>/post_comment/', comment_views.create_comment),
    path('comments/<int:comment_id>/approve/', comment_views.approve_comment),
    path('comments/<int:comment_id>/reject/', comment_views.reject_comment),
    path('blogs/<int:blog_id>/comments/', comment_views.get_blog_comments),
    path('comments/', comment_views.get_comments),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
