from django.urls import path

from . import views

app_name = 'grammar'

urlpatterns = [
    path('', views.topic_list, name='topic_list'),
    path('coach/', views.coach, name='coach'),
    path('<slug:slug>/', views.topic_detail, name='topic_detail'),
    path('<slug:slug>/exercise/', views.exercise, name='exercise'),
    path('<slug:slug>/exercise/<int:position>/', views.exercise_question, name='exercise_question'),
    path('<slug:slug>/results/', views.exercise_results, name='exercise_results'),
]
