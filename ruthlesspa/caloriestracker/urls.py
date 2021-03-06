from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='caloriestracker'),
    path('getMealCards/', views.BaseMealCardsViewSer.getMealCards, name='getMealCards'),
    path('postSaveMealCards/', views.BaseMealCardsViewSer.postSaveMealCards, name='postSaveMealCards'),
    path('getIngredientFromId/', views.BaseIngredientsView.getIngredientFromId, name='getIngredientFromId'),
    path('uuidGenerator/', views.uuidGenerator, name='uuidGenerator'),
    path('getStats/', views.UserStatistics.getStats, name='getStats'),
]