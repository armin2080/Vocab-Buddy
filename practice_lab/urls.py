from django.urls import path

from . import views


app_name = 'practice_lab'

urlpatterns = [
    path('', views.lab, name='lab'),
    path('<int:pk>/', views.session, name='session'),
    path('<int:pk>/close/', views.close_session, name='close_session'),
]
