# compliance/models.py

from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta

# 1. 雇主資料表 (employers)
class Employer(models.Model):
    company_name = models.CharField(max_length=100, verbose_name='公司名稱')
    tax_id = models.CharField(max_length=20, unique=True, verbose_name='統一編號')
    contact_person = models.CharField(max_length=50, blank=True, null=True, verbose_name='聯絡人')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='電話')

    class Meta:
        verbose_name = "雇主"
        verbose_name_plural = "雇主"

    def __str__(self):
        return self.company_name

# 2. 移工基本資料表 (workers)
class Worker(models.Model):
    arc_number = models.CharField(max_length=20, unique=True, verbose_name='居留證號')
    passport_number = models.CharField(max_length=20, verbose_name='護照號碼')
    full_name = models.CharField(max_length=100, verbose_name='移工全名')
    nationality = models.CharField(max_length=50, verbose_name='國籍')
    hire_date = models.DateField(verbose_name='僱用起始日期')

    # 外鍵：指向 Employer Model
    employer = models.ForeignKey(
        Employer, 
        on_delete=models.RESTRICT, # 不允許刪除仍有移工關聯的雇主
        verbose_name='所屬雇主'
    )

    is_active = models.BooleanField(default=True, verbose_name='是否在職')

    class Meta:
        verbose_name = "移工"
        verbose_name_plural = "移工"

    def __str__(self):
        return f"{self.full_name} ({self.arc_number})"

    def check_exam_status(self, exam_type: str):
        """
        檢查特定體檢類型（如 '6個月體檢'）的合規狀態。

        Args:
            exam_type (str): 體檢類別名稱。
        
        Returns:
            dict: 包含 'required_date' (應檢日期) 和 'is_compliant' (是否合格)
        """
        
        # 1. 計算應檢基準月數 (入境體檢是 0 個月)
        if exam_type == '入境體檢':
            months = 0
        elif exam_type == '6個月體檢':
            months = 6
        elif exam_type == '18個月體檢':
            months = 18
        elif exam_type == '30個月體檢':
            months = 30
        else:
            return None

        # 2. 計算應檢日期
        # 使用 relativedelta 處理月份增加，比直接加天數更準確
        required_date = self.hire_date + relativedelta(months=+months)
        
        # 3. 定義法規允許的體檢區間 (前後 30 天)
        start_date = required_date + relativedelta(days=-30)
        end_date = required_date + relativedelta(days=+30)

        # 4. 查詢是否有合格的體檢紀錄落在區間內
        has_passed_exam = self.medicalexam_set.filter( # worker.medicalexam_set 是 Django 自動產生的反向查詢名稱
            exam_type=exam_type,
            report_status='合格',
            exam_date__gte=start_date, # 大於或等於起始日
            exam_date__lte=end_date    # 小於或等於截止日
        ).exists()

        # 5. 判斷是否逾期/即將到期
        today = date.today()
        
        if has_passed_exam:
            status = '已合格'
        elif today > end_date:
            status = '已逾期'
        elif today >= start_date and today <= end_date:
            status = '應檢期內'
        elif today < start_date and (start_date - today).days <= 30:
            status = '即將到期 (30天內)'
        else:
            status = '未到期'

        return {
            'type': exam_type,
            'required_date': required_date,
            'status': status,
            'is_compliant': has_passed_exam
        }

# 3. 體檢紀錄表 (medical_exams)
class MedicalExam(models.Model):
    EXAM_TYPES = (
        ('入境體檢', '入境體檢'),
        ('6個月體檢', '6個月體檢'),
        ('18個月體檢', '18個月體檢'),
        ('30個月體檢', '30個月體檢'),
        ('其他', '其他'),
    )
    STATUS_CHOICES = (
        ('合格', '合格'),
        ('不合格', '不合格'),
        ('補檢中', '補檢中'),
        ('待審核', '待審核'),
        ('已完成', '已完成'),
    )

    # 外鍵：指向 Worker Model
    worker = models.ForeignKey(
        Worker, 
        on_delete=models.CASCADE, # 刪除移工時，體檢紀錄一併刪除
        verbose_name='移工'
    )
    exam_date = models.DateField(verbose_name='實際體檢日期')
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES, verbose_name='體檢類別')
    report_status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='報告狀態')

    expiry_date = models.DateField(blank=True, null=True, verbose_name='體檢有效期限')
    hospital_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='醫院名稱')
    report_document_url = models.TextField(blank=True, null=True, verbose_name='報告文件URL')

    class Meta:
        verbose_name = "體檢紀錄"
        verbose_name_plural = "體檢紀錄"
        # 確保同一個移工不會在同一天進行同類型體檢 (防止重複輸入)
        unique_together = ('worker', 'exam_type', 'exam_date') 

    def __str__(self):
        return f"{self.worker.full_name} - {self.exam_type} ({self.report_status})"