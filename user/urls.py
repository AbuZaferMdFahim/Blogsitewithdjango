from django.urls import path 
from .views import * 

urlpatterns = [
    path('login/',login_user,name='login_user'),
    path('logout/',logout_user,name='logout_user'),
    path('registration_user/', registration_user, name='registration_user'),
    path('profile/',profile,name='profile'),
    path('change_profile_image/', change_profile_image, name='change_profile_image'),
    path('userinformation/<str:username>/', userinformation, name='userinformation'),
    path('follow_unfollow_user/<int:user_id>/', follow_unfollow_user, name='follow_unfollow_user'),
    path('notification/',notification,name='notification'),
    path('mute/<int:user_id>/',mute,name='mute'),
]