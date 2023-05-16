from typing import Any, Optional
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.exceptions import ObjectDoesNotExist
from django.http.request import HttpRequest
from user.models import User

class EmailAuthentication(ModelBackend):
    def authenticate(self, request, username = None, password = None, *args, **kwargs):
        try :
            user = User.objects.get(email = username)
            if user.check_password(password):
                return user
            else: 
                return None
            
        except ObjectDoesNotExist:
            return None

    def get_user(self, user_id: int):
        try :
            user = User.objects.get(pk = user_id)
            return user       
        except ObjectDoesNotExist:
            return None