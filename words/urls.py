from django.urls import path
from . import views

app_name = 'words'

urlpatterns = [
    path('', views.word_list, name='word_list'),
    path('add/', views.add_word, name='add_word'),
    path('<int:pk>/', views.word_detail, name='word_detail'),
    path('<int:pk>/edit/', views.edit_word, name='edit_word'),
    path('<int:pk>/refresh/', views.refresh_word, name='refresh_word'),
    path('<int:pk>/delete/', views.delete_word, name='delete_word'),
]
