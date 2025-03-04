from django.urls import path
from .views import (
  Test, CompanyCreateView, CompanyListView, CompanyDetailView,ExportAllDataCSV
)

from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView,
)

urlpatterns = [
  path('test/', Test.as_view(), name='test'),
  path('companies/', CompanyCreateView.as_view(), name='company-create'),
  path('companies-list/', CompanyListView.as_view(), name='company-list'),
  path('companies-detail/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
  
  #for JWT
  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  
  #export CSV table
  path('export', ExportAllDataCSV.as_view(), name='export'),
]
