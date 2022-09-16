# 장고 폼
# 폼은 쉽게 말해 페이지 요청 시 전달되는 파라미터들을 쉽게 관리하기 위해 사용하는 클래스이다.
# 폼은 필수 파라미터의 값이 누락되지 않았는지, 파라미터의 형식은 적절한지 등을 검증할 목적으로 사용한다.
# 이 외에도 HTML을 자동으로 생성하거나 폼에 연결된 모델을 이용하여 데이터를 저장하는 기능도 있다.


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# UserForm은 django.contrib.auth.forms 모듈의 UserCreationForm 클래스를 상속하여 만들었다.
# UserForm을 따로 만들지 않고 UserCreationForm을 그대로 사용해도 되지만, 이메일 등의 추가적인 속성을 추가하기 위해서는 UserCreationForm 클래스를 상속하여 새 클래스를 만들어야 한다.
class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    class Meta:  # 이너 클래스인 Meta 클래스가 반드시 필요  # Meta 클래스에는 사용할 모델과 모델의 속성을 적어야 한다.
        model = User  # 사용할 모델
        fields = ("username", "password1", "password2", "email")  # UserForm에서 사용할 User 모델의 속성
        # username	사용자이름
        # password1	비밀번호1
        # password2	비밀번호2 (비밀번호1을 제대로 입력했는지 대조하기 위한 값)
        # UserCreationForm의 is_valid 함수는 폼에 위의 속성 3개가 모두 입력되었는지, 비밀번호1과 비밀번호2가 같은지, 비밀번호의 값이 비밀번호 생성 규칙에 맞는지 등을 검사하는 로직을 내부적으로 가지고 있다.
