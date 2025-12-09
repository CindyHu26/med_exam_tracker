# compliance/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('compliance/due/', views.ComplianceDueListView.as_view(), name='compliance_due'),
    # ... 可以加入其他 API 路徑 ...
]