from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('remove_missing_values/', views.remove_missing_values, name='remove_missing_values'), 
    path('fill_missing_values/', views.fill_missing_values, name='fill_missing_values'),
]
