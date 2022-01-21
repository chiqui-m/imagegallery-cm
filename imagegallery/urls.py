from django.urls import path
from . import views

app_name = "imagegallery"

urlpatterns = [
    path("", views.gallery, name="gallery"),      
	path("login/", views.loginUser, name="login"),
	path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerUser, name="register"),
    path("photo/<int:photo_id>/", views.photo, name="photo"),
    path("add/", views.add, name="add"),
    ]


