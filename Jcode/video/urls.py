from django.contrib import admin
from django.urls import path,re_path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index,name='index'),
    path('detail/<slug:slug>/', views.BookDetailView.as_view(), name='detail'),
    path("course/", views.management_course, name='management_course'),
    path("chapter/<int:id>", views.management_chapter, name="management_chapter"),
    path("lesson/<int:id>", views.management_lesson, name="management_lesson"),
    path('deletevideo/<int:id>', views.video_delete, name='video_delete'),
    path('deletechapter/<int:id>', views.chapter_delete, name='chapter_delete'),
    path('deletelesson/<int:id>', views.lesson_delete, name='lesson_delete'),
    path('updatevideo/<int:id>',views.update_video,name='update_course'),
    re_path(r'add/$', views.video_add, name='video_add'),
    re_path(r'addchapter/$', views.video_addchapter, name='video_addchapter'),
    re_path(r'addlesson/$', views.video_addlesson, name='video_addlesson'),
]
