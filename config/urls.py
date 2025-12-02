from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from configapp.views import TodoViewSet, UserViewSet

router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todos')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
