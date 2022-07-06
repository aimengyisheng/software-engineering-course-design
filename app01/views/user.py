from django.shortcuts import render, redirect
from app01 import models
from app01.utils.forms import UserModelForm, UserResetModelForm


def home(request, uid):
    """用户主页"""
    row_object = models.UserInfo.objects.filter(id=uid).first()
    company_name = row_object.company
    content = {'name': row_object.username, 'uid': uid, 'cname': company_name}
    if row_object.user_type == 1:
        return render(request, 'tourist_layout.html', content)
    if row_object.user_type == 2:
        return render(request, 'auth_layout.html', content)
    if row_object.user_type == 3:
        cid = company_name.id
        content['cid'] = cid
        return render(request, 'company_layout.html', content)
    if row_object.user_type == 4:
        return render(request, 'admin_layout.html', content)


def info(request, uid):
    """显示用户资料（支持编辑功能）"""

    row_object = models.UserInfo.objects.filter(id=uid).first()
    if row_object.user_type == 3:
        cname = row_object.company.company_name
        if request.method == "GET":
            # 根据id去数据库获取要编辑的数据
            form = UserModelForm(instance=row_object)
            return render(request, 'user_info.html',
                          {'form': form, 'cname': cname, 'name': row_object.username, 'uid': uid,
                           'type': row_object.user_type})
        form = UserModelForm(data=request.POST, instance=row_object)
        cname = request.POST.get('company')
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.company = models.CompanyInfo.objects.filter(company_name=cname).first()
            tmp.password = row_object.password
            tmp.save()  # 保存的是用户输入的所有数据
            return redirect('/home/' + str(uid) + '/')
        try:
            form.errors['company'][0] = '公司不存在，请联系管理员添加公司'
            return render(request, 'user_info.html',
                          {'form': form, 'cname': cname, 'name': row_object.username, 'uid': uid,
                           'type': row_object.user_type})
        except:
            return render(request, 'user_info.html',
                          {'form': form, 'cname': cname, 'name': row_object.username, 'uid': uid,
                           'type': row_object.user_type})
    else:
        if request.method == "GET":
            # 根据id去数据库获取要编辑的数据
            form = UserModelForm(instance=row_object)
            return render(request, 'user_info.html',
                          {'form': form, 'name': row_object.username, 'uid': uid, 'type': row_object.user_type})
        form = UserModelForm(data=request.POST, instance=row_object)
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.password = row_object.password
            tmp.save()  # 保存的是用户输入的所有数据
            return redirect('/home/' + str(uid) + '/')
        return render(request, 'user_info.html',
                      {'form': form, 'name': row_object.username, 'uid': uid, 'type': row_object.user_type})


def password_reset(request, uid):
    """密码重置"""
    row_obj = models.UserInfo.objects.filter(id=uid).first()
    title = "重置密码 - {}".format(row_obj.username)
    if request.method == "GET":
        form = UserResetModelForm()
        return render(request, 'change.html', {'form': form, 'title': title})
    form = UserResetModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect('/user/' + str(uid) + '/info/')
    return render(request, 'change.html', {'form': form, 'title': title})
