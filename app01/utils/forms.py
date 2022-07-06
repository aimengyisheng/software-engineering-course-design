from django import forms
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from django.core.exceptions import ValidationError

from app01.utils.encrypt import md5


class UserModelForm(BootStrapModelForm):
    # name = forms.CharField(min_length=3, label="用户名")
    # password = forms.CharField(label="密码")  # validators正则表达式验证

    # mobile = forms.CharField(label="手机号", validators=[RegexValidator(r'^1[3-9]\d{9}
    # def clean_moblie(self):
    #     input = self.cleaned_data['mobile']
    #     if len(input) != 11:
    #         raise ValidationError("格式错误")
    #     return input

    class Meta:
        model = models.UserInfo
        # fields = ["name", "password", "age", 'username', 'gender', 'depart']
        fields = ['username', 'phone_no', 'company', 'person_id']
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"})
        # }


class RouteModelEditForm(BootStrapModelForm):
    company = forms.CharField(disabled=True)

    def clean_company(self):
        cid = self.cleaned_data['company']
        return models.CompanyInfo.objects.filter(id=cid).first()

    class Meta:
        model = models.RouteInfo
        fields = '__all__'
        widgets = {
            'begin_time': forms.DateInput(attrs={"type": "Date"}),
            'end_time': forms.DateInput(attrs={'type': 'Date'}),
            'order_ddl': forms.DateInput(attrs={'type': 'Date'}),
        }


class SceneModelForm(BootStrapModelForm):
    class Meta:
        model = models.SceneInfo
        fields = '__all__'
        widgets = {
            'scenic_time': forms.DateInput(attrs={"type": 'Date'})
        }


class NewsModelForm(BootStrapModelForm):
    class Meta:
        model = models.TravelNewsInfo
        fields = '__all__'
        widgets = {
            'news_date': forms.DateInput(attrs={"type": 'Date'})
        }


class RouteModelAddForm(BootStrapModelForm):
    class Meta:
        model = models.RouteInfo
        fields = '__all__'
        widgets = {
            'begin_time': forms.DateInput(attrs={"type": "Date"}),
            'end_time': forms.DateInput(attrs={'type': 'Date'}),
            'order_ddl': forms.DateInput(attrs={'type': 'Date'}),
        }


class UserRegisterModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = models.UserInfo
        fields = ['username', 'password', 'confirm_password', 'phone_no', 'user_type', 'company', 'person_id']
        widgets = {
            "password": forms.PasswordInput
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        # 返回什么，此字段保存到数据库就是什么
        return confirm


class UserResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = models.UserInfo
        fields = ['password', 'confirm_password']
        widgets = {
            "password": forms.PasswordInput
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pwd = md5(pwd)
        exists = models.UserInfo.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("密码不能与之前一致")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != pwd:
            raise ValidationError("密码不一致")
        # 返回什么，此字段保存到数据库就是什么
        return confirm


class TouristBRModelForm(BootStrapModelForm):
    class Meta:
        model = models.OrderedRouteInfo
        fields = '__all__'
