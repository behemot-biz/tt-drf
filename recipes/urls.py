from django.urls import path
from recipes import views

urlpatterns = [
    path('recipes/', views.RecipeList.as_view()),
    path(
        'recipe-ingredients/', 
        views.RecipeIngredientListView.as_view(), 
        name='recipe-ingredient-list'
        ),
]