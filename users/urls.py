from django.urls import path,include
from users import views
from django.contrib.auth import views as auth_views #import this

urlpatterns = [
    path('robots.txt/', views.get_robot_file,name="robots"),
    path('signup/', views.signupUser, name="signup"),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logout_request, name= "logout"),
    path('profile/edit/',views.profile_edit, name="profile_add"),

    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]