
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from base.views import *
from django.conf import settings
from django.conf.urls.static import static





router = DefaultRouter()
router.register(r'api/categories', CategorieViewSet, basename='categories')
router.register(r'api/composants', ComposantViewSet, basename='composants')
router.register(r'api/equipements', EquipementViewSet, basename='equipements')
router.register(r'api/interventions', InterventionViewSet, basename='interventions')
router.register(r'api/demandes', DemandeViewSet, basename='demandes')


urlpatterns = [
    path('', include(router.urls)),
    path('api/admin/users/create/', AdminCreateUserView.as_view(), name='admin-create-user'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/admin/users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('api/admin/users/<int:pk>/', AdminUserDetailView.as_view(), name='admin-user-detail'),
    path('api/admin/users/<int:pk>/password/', AdminPasswordUpdateView.as_view(), name='admin-password-update'),
    path('admin/', admin.site.urls),
    path('api/dashboard/', DashboardAPIView.as_view(), name='dashboard'),
    path('api/equipements-export-pdf/', export_equipements_pdf, name='equipement-export-pdf'),
    path('api/media/', MediaListView.as_view(), name='media-list'),
    path('send-html-email/', DynamicHTMLEmailView.as_view(), name='send_html_email'),


    ]



from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)