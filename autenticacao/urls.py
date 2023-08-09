from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import home, ChangePasswordView, RequestPasswordResetView, ResetPasswordView

urlpatterns = [
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('home/', home, name='home'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('request-password-reset/', RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('reset-password/<str:uidb64>/<str:token>/', ResetPasswordView.as_view(), name='reset-password'),
]