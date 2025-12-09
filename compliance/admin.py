from django.contrib import admin
from .models import Employer, Worker, MedicalExam

# 1. 雇主 Admin 優化
@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'tax_id', 'contact_person', 'phone')
    search_fields = ('company_name', 'tax_id')

# 2. 移工 Admin 優化 (重點)
class MedicalExamInline(admin.TabularInline):
    """將體檢紀錄嵌入到移工的詳細頁面"""
    model = MedicalExam
    extra = 0 # 不預設顯示空白行
    # 顯示重要的欄位
    fields = ('exam_type', 'exam_date', 'report_status', 'expiry_date')
    readonly_fields = fields # 設置為只讀（如果您希望只能在專門頁面新增）

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    # 在清單頁面顯示的欄位
    list_display = ('full_name', 'arc_number', 'employer', 'hire_date', 'is_active')
    # 可以點擊連結進入詳細頁面的欄位
    list_display_links = ('full_name', 'arc_number')
    # 篩選器（右側欄）
    list_filter = ('is_active', 'nationality', 'employer')
    # 搜尋欄
    search_fields = ('full_name', 'arc_number', 'passport_number')
    # 編輯頁面的欄位分組
    fieldsets = (
        ('基本資料', {
            'fields': ('full_name', 'nationality', 'is_active', 'employer'),
        }),
        ('證件資訊與日期', {
            'fields': ('arc_number', 'passport_number', 'hire_date'),
        }),
    )
    # 內嵌體檢紀錄
    inlines = [MedicalExamInline]

# 3. 體檢紀錄 Admin 優化
@admin.register(MedicalExam)
class MedicalExamAdmin(admin.ModelAdmin):
    list_display = ('worker_name', 'exam_type', 'exam_date', 'report_status')
    list_filter = ('exam_type', 'report_status', 'exam_date')
    search_fields = ('worker__full_name', 'worker__arc_number', 'hospital_name')
    # 允許通過外鍵欄位直接搜尋
    raw_id_fields = ('worker',)

    # 自訂顯示移工姓名（因為我們需要通過外鍵訪問）
    def worker_name(self, obj):
        return obj.worker.full_name
    worker_name.short_description = '移工姓名'