from django import forms

from sp_user.helper import set_password
from sp_user.models import Users


# 注册
class RegisterModelForm(forms.ModelForm):
    password1 = forms.CharField(max_length=16,
                                min_length=6,
                                error_messages={
                                    'required': '密码必须填写',
                                    'max_length': '密码长度不能超过16个字符',
                                    'min_length': '密码长度必须大于6个'
                                }
                                )
    password2 = forms.CharField(max_length=16,
                                min_length=6,
                                error_messages={
                                    'required': '密码必须填写',
                                    'max_length': '密码长度不能超过16个字符',
                                    'min_length': '密码长度必须大于6个'
                                }

                                )

    class Meta:
        model = Users
        fields = ['phone', ]
        error_messages = {
            'phone': {
                'required': '手机号码必须填写'
            }
        }

    def clean_password2(self):
        pwd1 = self.cleaned_data.get('password1')
        pwd2 = self.cleaned_data.get('password2')

        if pwd1 != pwd2 and pwd1 and pwd2:
            raise forms.ValidationError('请重新输入密码,您的两次密码输入不一致')
        return pwd2

    # 验证手机号是不是唯一
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        rs = Users.objects.filter(phone=phone).exists()
        if rs:
            raise forms.ValidationError('手机号码已经注册')
        return phone


# 登录
class LoginForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['phone', 'password']
        error_messages = {
            'phone': {
                'required': '手机号码必须填写',
            },
            'password': {
                'required': '密码未填写,请填写',
                'min_length': '密码不得小于6个',
                'max_length': '密码不得大于64个',
            }
        }

    widgets = {
        'phone': forms.TextInput(attrs={'class': 'login-name', 'placeholder': '请输入手机号'}),
        'password': forms.PasswordInput(attrs={'class': 'login-password', 'placeholder': '请输入密码'}),
    }

    def clean(self):
        cleaned_data = self.cleaned_data
        # 获取数据
        phone = cleaned_data.get('phone')
        password = cleaned_data.get('password')
        # 验证手机号码是否存在
        if all([phone, password]):
            # 根据手机号码获取用户
            try:
                user = Users.objects.get(phone=phone)
            except Users.DoesNotExist:
                raise forms.ValidationError({"phone": "该用户不存在!"})
            # 判断密码是否正确
            if user.password != set_password(password):
                raise forms.ValidationError({"password": "密码填写错误!"})
            # 将用户信息保存到cleaned_data中
            cleaned_data['user'] = user
            return cleaned_data
        else:
            return cleaned_data


# 修改
class UserChangeModelForm(forms.ModelForm):
    class Meta:
        model = Users
        # 排除不用的字段
        exclude = ['create_time,', 'update_time', 'is_delete', 'password']
        # 修改的样式
        widgets = {
            "nickname": forms.TextInput(attrs={'class': "infor-tele", "placeholder": "请填写昵称"}),
            "gender": forms.RadioSelect(),
            "birthday": forms.DateInput(attrs={'class': "infor-tele", "type": 'date'}, format='%Y-%m-%d'),
            "school_name": forms.TextInput(attrs={'class': "infor-tele", "placeholder": "请输入学校"}),
            "address": forms.TextInput(attrs={'class': "infor-tele", "placeholder": "请输入地址"}),
            "hometown": forms.TextInput(attrs={'class': "infor-tele", "placeholder": "请输入老家"}),
            "phone": forms.TextInput(attrs={'class': "infor-tele", "placeholder": "请输入手机号"}),
        }

    def validate_unique(self):
        pass
