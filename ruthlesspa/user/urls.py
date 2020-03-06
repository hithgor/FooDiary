from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('login/', views.CreateUserView.login, name='login'),
    path('logout/', views.CreateUserView.logout, name='logout'),
]
