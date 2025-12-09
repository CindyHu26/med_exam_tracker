from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import Worker
from .serializers import WorkerComplianceSerializer

class ComplianceDueListView(APIView):
    """
    獲取即將到期/已逾期體檢的移工清單
    只允許具備管理員權限的使用者存取。
    """
    # 應用權限檢查：只允許 IsAdminUser 通過
    permission_classes = [IsAdminUser]
    
    def get(self, request, *args, **kwargs):

        # 1. 取得所有在職移工，並優化查詢
        workers = Worker.objects.filter(is_active=True).select_related('employer')

        due_list = []

        # 2. 遍歷移工並進行序列化
        for worker in workers:
            serializer = WorkerComplianceSerializer(worker)
            data = serializer.data

            # 3. 檢查序列化後的數據中是否有需要警示的狀態 (沿用舊有邏輯)
            alert_needed = any(
                status['status'] in ['已逾期', '應檢期內', '即將到期 (30天內)']
                for status in data['exam_statuses']
            )

            if alert_needed:
                due_list.append(data) # 直接添加序列化後的數據

        return Response(due_list)