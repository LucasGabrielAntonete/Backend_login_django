from django.contrib import admin
from django.urls import path, include, re_path
from usuario.router import router as usuario_router
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from usuario.utils.cadastro import cadastro
from usuario.utils.login import login
from usuario.utils.authgoogle import register_by_access_token, authentication_test

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(usuario_router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/cadastro/", cadastro, name="cadastro"),
    path("api/login/", login, name="login"),
    path('api/authentication-test/', authentication_test),
    re_path('api/register-by-access-token/' + r'social/(?P<backend>[^/]+)/$', register_by_access_token),
]
