from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.createInactive, name='create'),
    path('login/', views.CreateUserView.login, name='login'),
    path('logout/', views.CreateUserView.logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.CreateUserView.activate, name='activate'),
]
