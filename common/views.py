# 장고 뷰
# 장고에서 뷰는 어떤 데이터를 표시할지 정의하며, HTTP 응답 상태 코드(response)를 반환한다.
# views.py 파일에 애플리케이션의 처리 논리를 정의한다.
# 사용자가 입력한 URL에 따라, 모델(Model)에서 필요한 데이터를 가져와 뷰에서 가공해 보여주며, 템플릿(Template)에 전달하는 역할을 한다.
# 장고의 뷰 파일(views.py)은 요청에 따른 처리 논리를 정의한다.
# 즉, 사용자가 요청하는 값(request)을 받아 모델과 템플릿을 중개하는 역할을 한다.


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm

# Create your views here.


# 회원가입 관련 함수 뷰
def signup(request):
    # POST 요청 방식
    if request.method == "POST":
        # (common/forms.py의) UserForm으로부터 폼 데이터를 전달받음
        form = UserForm(request.POST)
        # POST 요청인 경우에는, 화면에서 입력한 데이터로 사용자를 생성
        if form.is_valid():
            form.save()
            # form.cleaned_data.get 함수 : 폼의 입력값을 개별적으로 얻고 싶은 경우에 사용하는 함수로, 여기서는 인증 시 사용할 사용자명과 비밀번호를 얻기 위해 사용
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # 신규 사용자를 생성한 후에 자동 로그인 될 수 있도록 authenticate와 login 함수 사용
            # django.contrib.auth.authenticate : 사용자 인증을 담당 (사용자명과 비밀번호가 정확한지 검증한다.)
            # django.contrib.auth.login : 로그인을 담당 (사용자 세션을 생성한다.)
            user = authenticate(username=username, password=raw_password)
            # 해당 사용자로 로그인 시킴
            login(request, user)
            return redirect('index')
    # GET 요청 방식
    else:
        # (common/forms.py의) UserForm으로부터 폼 데이터를 전달받음
        form = UserForm()
    # GET 요청인 경우에는, 회원가입 화면을 보여준다.
    return render(request, 'common/signup.html', {'form': form})