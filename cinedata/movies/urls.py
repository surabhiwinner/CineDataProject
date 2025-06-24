from django.urls import path

from . import views


urlpatterns = [
    path('movies/', views.MoviesListCreateView.as_view()),

    path('movies/<str:uuid>/',views.MovieRetrieveUpdateDestroyView.as_view()),

    path('rating/<str:uuid>/', views.AddRatingview.as_view()),

    path('top-20-movies/',views.Top20MoviesListView.as_view())

    ]

