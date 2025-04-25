
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from base.views import *





router = DefaultRouter()
router.register(r'api/categories', CategorieViewSet, basename='categories')
router.register(r'api/composants', ComposantViewSet, basename='composants')
router.register(r'api/equipements', EquipementViewSet, basename='equipements')


urlpatterns = [
    path('', include(router.urls)),
    path('api/admin/users/create/', AdminCreateUserView.as_view(), name='admin-create-user'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/admin/users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('api/admin/users/<int:pk>/', AdminUserDetailView.as_view(), name='admin-user-detail'),
    path('api/admin/users/<int:pk>/password/', AdminPasswordUpdateView.as_view(), name='admin-password-update'),
    path('admin/', admin.site.urls),
    ]