from django import  forms

from apps.user.models import Users


class TodoAddForm(forms.Form):
    title = forms.CharField(max_length=30,min_length=5)
    finish_date = forms.DateField()
    content = forms.CharField(max_length=225)

class TodoUpdateModelForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = '__all__'
        error_messages = {
            'title':{
                'required':'标题必须填写',
                'max_length':'最大长度不能大于50',
            },
            'finish_date':{
                'required':'时间必须填写',
            },
            'content':{
                'required':'内容必须填写',
            }
        }