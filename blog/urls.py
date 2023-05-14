from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('blogs/',blogs,name='blogs'),
    path('category_blogs/<str:slug>/',category_blogs,name='category_blogs'),
    path('tag_blogs/<str:slug>/',tag_blogs,name='tag_blogs'),
    path('blogs/<str:slug>/', blog_details, name='blog_details'),
    path('blogs/<int:blog_id>/<int:comment_id>/', add_reply, name='add_reply'),
    path('likeblogs/<int:pk>/', likeblog, name='likeblog'),
    path('search_blogs/', search_blogs,name="search_blogs"),
    path('myblogs/', myblogs,name="myblogs"),
    path('addblogs/', addblogs,name="addblogs"),
    path('updateblogs/<str:slug>/', updateblogs,name="updateblogs"),
]