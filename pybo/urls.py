# 장고 URL
# 장고에서 URL은 URL 경로와 일치하는 뷰(View)를 매핑(Mapping)하거나 라우팅(Routing)하는 역할을 한다.
# 즉, 장고에서 URL 설정은 하나의 항목을 연결하는 퍼머링크(Permalink)를 생성하거나 쿼리스트링(Query string) 등을 정의할 수 있다.
# urls.py 파일에 URL 경로에 관한 논리를 정의한다.


from django.urls import path

from .views import base_views, question_views, answer_views


# URL 네임스페이스 설정
app_name = 'pybo'

urlpatterns = [
    # base_views.py
    #
    # index 페이지 URL 매핑
    # name='index' : 해당 URL에 대해 URL 별칭 설정
    path('', base_views.index, name='index'),
    # 질문 상세 페이지 URL 매핑
    # <int:question_id> : 정수 숫자 매핑
    # 예를 들어, http://localhost:8000/pybo/2/ 페이지가 요청되면
    # 여기에 등록한 매핑 룰에 의해 http://localhost:8000/pybo/<int:question_id>/ 가
    # 적용되어 question_id 에 2가 저장되고, views.detail 함수도 실행
    # name='detail' : 해당 URL에 대해 URL 별칭 설정
    path('<int:question_id>/', base_views.detail, name='detail'),

    # question_views.py
    #
    # 질문 등록 기능 URL 매핑
    # name='question_create' : 해당 URL에 대해 URL 별칭 설정
    path('question/create/', question_views.question_create, name='question_create'),
    # 질문 수정 기능 URL 매핑
    # name='question_modify' : 해당 URL에 대해 URL 별칭 설정
    path('question/modify/<int:question_id>/', question_views.question_modify, name='question_modify'),
    # 질문 삭제 기능 URL 매핑
    # name='question_delete' : 해당 URL에 대해 URL 별칭 설정
    path('question/delete/<int:question_id>/', question_views.question_delete, name='question_delete'),
    # 질문 추천 기능 URL 매핑
    path('question/vote/<int:question_id>/', question_views.question_vote, name='question_vote'),

    # answer_views.py
    # 답변 등록 기능 URL 매핑
    # 예를 들어, http://locahost:8000/pybo/answer/create/2/ 페이지가 요청되면
    # 여기에 등록한 매핑 룰에 의해 http://localhost:8000/pybo/answer/create/<int:question_id>/ 가
    # 적용되어 question_id 에 2가 저장되고, views.answer_create 함수도 실행
    # name='answer_create' : 해당 URL에 대해 URL 별칭 설정
    path('answer/create/<int:question_id>/', answer_views.answer_create, name='answer_create'),
    # 답변 수정 기능 URL 매핑
    path('answer/modify/<int:answer_id>/', answer_views.answer_modify, name='answer_modify'),
    # 답변 삭제 기능 URL 매핑
    path('answer/delete/<int:answer_id>/', answer_views.answer_delete, name='answer_delete'),
    # 답변 추천 기능 URL 매핑
    path('answer/vote/<int:answer_id>/', answer_views.answer_vote, name='answer_vote'),
]
