from django.urls import path
from . import views

app_name = 'learning'

urlpatterns = [
    path('', views.index, name='index'),
    path('review/start/', views.review_start, name='review_start'),
    path('review/next/', views.review_next, name='review_next'),
    path('verb/<str:verb>/', views.verb_info, name='verb_info'),
]
