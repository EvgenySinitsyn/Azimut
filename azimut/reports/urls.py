from django.urls import path, include
from .views import index, result, LoginUserView, logout_user

urlpatterns = [
    path('', result, name='result'),
    path('download/', index),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]