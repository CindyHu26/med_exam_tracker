# compliance/urls.py

from django.urls import path
# 1. 匯入 DRF 的認證視圖
from rest_framework.authtoken import views as auth_views 

# 2. 匯入您自定義的視圖 (為了避免命名衝突，給它一個別名)
from . import views as compliance_views 

urlpatterns = [
    # 核心預警 API (使用您自定義的視圖)
    path('compliance/due/', compliance_views.ComplianceDueListView.as_view(), name='compliance_due'),

    # 登入 API (使用 DRF 匯入的視圖)
    path('auth/token/', auth_views.obtain_auth_token, name='api_token_auth'), 
]