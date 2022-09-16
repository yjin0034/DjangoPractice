from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer


# 답변 등록 관련 함수
# @login_required 어노테이션 : 로그인이 필요한 함수를 의미
# @login_required 어노테이션은 login_url='common:login' 처럼 로그인 URL을 지정할 수 있다.
# 로그아웃 상태에서 @login_required 어노테이션이 적용된 함수가 호출되면 자동으로 로그인 화면(login_url='common:login')으로 이동하게 됨
@login_required(login_url='common:login')
def answer_create(request, question_id):
    # 전달받은 id에 해당하는 (Question의) 질문 데이터 얻기
    question = get_object_or_404(Question, pk=question_id)
    # POST 요청 방식
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            # 답변의 글쓴이
            # author 속성에 로그인 계정 저장  # request.user : 현재 로그인한 계정의 User 모델 객체
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            # redirect 함수 : 페이지 이동을 위한 함수
            # 답변을 생성한 후 질문 상세 화면을 다시 보여주기 위해 redirect 함수를 사용  # pybo:detail 별칭에 해당하는 페이지로 이동
            # pybo:detail 별칭에 해당하는 URL은 question_id가 필요하므로 question.id를 인수로 전달
            # '{}#answer_{}'.format(resolve_url()) : 작성, 수정, 추천한 답변글 위치로 다시 이동시키는 앵커 태그 관련 코드
            # resolve_url : 실제 호출되는 URL 문자열을 리턴하는 장고의 함수
            # pybo:detail URL에 #answer_2와 같은 앵커를 추가하기 위해 resolve_url 함수를 사용
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=question.id), answer.id))
    # GET 요청 방식
    # (특정) 질문 화면에서 로그인 하지 않은 상태에서 '답변등록' 버튼을 클릭한 경우, /pybo/answer/create/ 페이지가 GET 방식으로 요청되어 answer_create 함수가 실행
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

# 답변 수정 관련 함수
@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정 권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)

# 답변 삭제 관련 함수
@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제 권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)

# 답변 추천 관련 함수
@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    # 본인 추천을 방지하기 위해, 로그인한 사용자와 추천하려는 질문의 글쓴이가 동일할 경우에는 추천할 수 없게 함.
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        # Question 모델의 voter는 여러 사람을 추가할 수 있는 ManyToManyField이므로, question.voter.add(request.user) 처럼 add 함수를 사용하여 추천인을 추가한다.
        # 동일한 사용자가 동일한 질문을 여러 번 추천하더라도 추천수가 증가하지는 않는다. ManyToManyField 내부에서 자체적으로 이와 같이 처리한다.
        answer.voter.add(request.user)
    # 질문 상세 페이지로 이동
    return redirect('{}#answer_{}'.format(
        resolve_url('pybo:detail', question_id=answer.question.id), answer.id))