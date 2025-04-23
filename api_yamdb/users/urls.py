from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, signup, generate_token


v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', generate_token, name='token'),
]
