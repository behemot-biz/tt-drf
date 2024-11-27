from django.urls import path
from recipes import views

urlpatterns = [
    path('recipes/', views.RecipeList.as_view()),
    path('recipes/<int:pk>/', views.RecipeDetail.as_view()),
    path('ingredients/', views.RecipeIngredientList.as_view()),
    path('ingredients/<int:pk>/', views.RecipeIngredientDetail.as_view()),
]