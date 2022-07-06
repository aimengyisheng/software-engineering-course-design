from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from io import BytesIO
from app01 import models
from app01.utils.bootstrap import BootStrapForm
from app01.utils.encrypt import md5
from app01.utils.code import check_code
from app01.utils.forms import UserRegisterModelForm


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput,
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


def login(request):
    """登录"""
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user_input_code = form.cleaned_data.pop('code')
        img_code = request.session.get('image_code', '')
        if img_code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {'form': form})
        user_object = models.UserInfo.objects.filter(**form.cleaned_data).first()
        if not user_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})
        # 用户名和密码正确
        # 网站生成随机字符串，写到用户浏览器的cookie中,再写入session中
        request.session['info'] = {'id': user_object.id, 'name': user_object.username}
        # session可以保存七天
        request.session.set_expiry(60 * 60 * 24 * 7)
        return redirect('/home/' + str(user_object.id))
    return render(request, 'login.html', {'form': form})


def logout(request):
    """注销"""
    request.session.clear()
    return redirect('/login/')


def image_code(request):
    """生成图片验证码"""
    # 调用pillow函数，生成图片
    img, code_string = check_code()
    # 把验证码文本写入session
    request.session['image_code'] = code_string
    # 给session设置60s超时
    request.session.set_expiry(60)
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def register(request):
    title = '用户注册'
    error = ''
    if request.method == "GET":
        form = UserRegisterModelForm()
        return render(request, 'register.html', {'form': form, 'title': title})
    form = UserRegisterModelForm(data=request.POST)
    cname = request.POST.get('company')
    form.company = cname
    if form.is_valid():
        if form.cleaned_data.get('user_type') == 3:
            if not cname:
                form.add_error('company', '公司不能为空')
            else:
                form.save()
                return redirect('/login/')
        elif form.cleaned_data.get('user_type') != 4:
            form.save()
            return redirect('/login/')
        else:
            form.add_error('user_type', '权限不足')
    try:
        if cname:
            form.errors['company'][0] = '公司不存在，请联系管理员添加'
        return render(request, 'register.html', {'form': form, 'title': title})
    except:
        return render(request, 'register.html', {'form': form, 'title': title})
