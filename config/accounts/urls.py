from django.urls import path
from. views import RegisterView , LoginView ,ProfileView,AdminUsersView
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import (SpectacularAPIView,SpectacularSwaggerView,SpectacularRedocView)


urlpatterns = [
    path('account/Register',RegisterView.as_view(), name='register'),
    path('account/Login',LoginView.as_view(),name='login'),
    path('account/profile',ProfileView.as_view(),name='profile'),
    path('account/Admin',AdminUsersView.as_view(),name='Admin'),
    path(
        'account/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
     # Swagger Schema
    path('account/schema/',SpectacularAPIView.as_view(),name='schema'),

    # Swagger UI
    path('account/docs/',SpectacularSwaggerView.as_view(url_name='schema'),name='swagger-ui'),

    # ReDoc
    path('account/redoc/',SpectacularRedocView.as_view(url_name='schema'),name='redoc'),

    # Re_n@d2er
]

