from django.urls import path

from .views import MoviesDetailApi, MoviesListApi

urlpatterns = [
    path('movies/<uuid:id>', MoviesDetailApi.as_view()),
    path('movies/', MoviesListApi.as_view()),
]
