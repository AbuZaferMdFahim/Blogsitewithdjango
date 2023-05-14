from django.urls import path 
from .views import * 

urlpatterns = [
    path('login/',login_user,name='login_user'),
    path('logout/',logout_user,name='logout_user'),
    path('registration_user/', registration_user, name='registration_user'),
    path('profile/',profile,name='profile'),
    path('change_profile_image/', change_profile_image, name='change_profile_image')
]