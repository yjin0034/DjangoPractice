from django.contrib import admin
from .models import Question


# Register your models here.

# Question 모델에 세부 기능을 추가할 QuestionAdmin 클래스 생성
class QuestionAdmin(admin.ModelAdmin):
    # 제목 검색 기능 추가
    search_fields = ['subject']

# Question 모델을 장고 관리자에 등록
# QuestionAdmin 클래스의 내용도 반영하며, Question 모델을 관리자에 등록?
admin.site.register(Question, QuestionAdmin)

