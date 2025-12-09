from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import Worker

class ComplianceDueListView(APIView):
    """
    獲取即將到期/已逾期體檢的移工清單
    只允許具備管理員權限的使用者存取。
    """
    # 應用權限檢查：只允許 IsAdminUser 通過
    permission_classes = [IsAdminUser]
    
    def get(self, request, *args, **kwargs):

        # 1. 取得所有在職移工
        workers = Worker.objects.filter(is_active=True).prefetch_related('medicalexam_set')

        due_list = []

        # 2. 遍歷每個移工
        for worker in workers:
            alert_needed = False
            worker_data = {
                'worker_id': worker.id,
                'full_name': worker.full_name,
                'arc_number': worker.arc_number,
                'hire_date': worker.hire_date,
                'employer_name': worker.employer.company_name,
                'exam_statuses': []
            }

            # 3. 檢查所有四個體檢週期
            for exam_type in ['入境體檢', '6個月體檢', '18個月體檢', '30個月體檢']:
                status_data = worker.check_exam_status(exam_type)

                if status_data:
                    worker_data['exam_statuses'].append({
                        'type': status_data['type'],
                        'required_date': status_data['required_date'],
                        'status': status_data['status'],
                    })

                    # 4. 設定警示條件：只要有 '已逾期' 或 '應檢期內' 就需要警示
                    if status_data['status'] in ['已逾期', '應檢期內', '即將到期 (30天內)']:
                        alert_needed = True

            # 5. 只將需要警示的移工加入清單
            if alert_needed:
                due_list.append(worker_data)

        return Response(due_list)