# compliance/serializers.py

from rest_framework import serializers
from .models import Worker, MedicalExam

# 1. 體檢紀錄序列化器
class MedicalExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalExam
        # 僅序列化前端 App 所需的欄位
        fields = ('exam_type', 'exam_date', 'report_status', 'expiry_date')

# 2. 移工序列化器 (包含體檢狀態邏輯)
class WorkerComplianceSerializer(serializers.ModelSerializer):
    # 這是為了確保我們能序列化雇主名稱，而不是只返回 ID
    employer_name = serializers.CharField(source='employer.company_name', read_only=True)
    
    # 新增一個欄位來存放計算出的體檢狀態清單
    exam_statuses = serializers.SerializerMethodField()

    class Meta:
        model = Worker
        fields = ('id', 'full_name', 'arc_number', 'hire_date', 'employer_name', 'exam_statuses')
        read_only_fields = fields # 這是只讀 API，所有欄位都應為只讀

    def get_exam_statuses(self, obj):
        """
        覆寫方法：計算並返回移工所有體檢週期的狀態
        """
        statuses = []
        for exam_type in ['入境體檢', '6個月體檢', '18個月體檢', '30個月體檢']:
            # 呼叫 Worker Model 內定義的核心檢查方法
            status_data = obj.check_exam_status(exam_type) 
            if status_data:
                statuses.append({
                    'type': status_data['type'],
                    'required_date': status_data['required_date'],
                    'status': status_data['status'],
                })
        return statuses