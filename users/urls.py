from django.urls import path,include
from users import views

urlpatterns = [
    path('robots.txt/', views.get_robot_file,name="robots"),
    path('signup/', views.signupUser, name="signup"),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logout_request, name= "logout"),
    path('profile/edit/',views.profile_edit, name="profile_add"),
]