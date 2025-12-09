from django.contrib import admin
from .models import Employer, Worker, MedicalExam

# 簡單註冊
admin.site.register(Employer)
admin.site.register(Worker)
admin.site.register(MedicalExam)