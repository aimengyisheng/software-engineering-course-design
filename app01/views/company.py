from django.core.exceptions import ValidationError
from django.db.models.functions import Concat
from django.shortcuts import render, redirect

from app01 import models
from app01.utils.forms import UserModelForm, RouteModelEditForm, RouteModelAddForm
from app01.utils.pagination import Pagination


def home(request, uid):
    """旅游公司信息管理主页"""
    obj = models.UserInfo.objects.filter(id=uid).first()
    cid = models.CompanyInfo.objects.filter(company_name=obj.company).first().id
    return render(request, 'company_layout.html', {'uid': uid, 'cid': cid})


def route_list(request, uid):
    """旅游公司线路列表"""
    row_obj = models.UserInfo.objects.filter(id=uid).first()
    cname = row_obj.company
    name = row_obj.username
    cid = cname.id
    cname = cname.company_name
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict["content__contains"] = search_data
    queryset = models.RouteInfo.objects.filter(**data_dict).filter(company=cid)
    page_object = Pagination(request, queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    context = {"queryset": page_queryset,
               "search_data": search_data,
               "page_string": page_string,
               "uid": uid,
               "name": name,
               "cname": cname}
    return render(request, 'route_list.html', context)


def route_delete(request, uid, rid):
    """删除路线"""
    models.RouteInfo.objects.filter(id=rid).delete()
    return redirect('/company/' + str(uid) + '/route/list/')


def route_edit(request, uid, rid):
    """编辑路线"""
    row_object = models.RouteInfo.objects.filter(id=rid).first()
    name = models.UserInfo.objects.filter(id=uid).first().username
    if request.method == "GET":
        # 根据id去数据库获取要编辑的数据
        form = RouteModelEditForm(instance=row_object)
        return render(request, 'route_edit.html', {'form': form, 'uid': uid, 'name': name})
    form = RouteModelEditForm(data=request.POST, instance=row_object)
    if form.is_valid():
        start = form.cleaned_data.get('begin_time')
        end = form.cleaned_data.get('end_time')
        ddl = form.cleaned_data.get('order_ddl')
        if end >= start >= ddl:
            form.save()  # 保存的是用户输入的所有数据
            # form.instance.字段名=值
            return redirect('/company/' + str(uid) + '/route/list/')
        if end < start:
            form.add_error('end_time', '结束时间应不早于开始时间')
        if ddl > start:
            form.add_error('order_ddl', '最晚预定时间应早于开始时间')
    return render(request, 'route_edit.html', {'form': form, 'uid': uid, 'name': name})


def route_add(request, uid):
    """添加路线"""
    row_obj = models.UserInfo.objects.filter(id=uid).first()
    name = row_obj.username
    cname = row_obj.company
    cid = cname.id
    if request.method == "GET":
        form = RouteModelAddForm()
        return render(request, 'route_add.html', {"form": form, 'uid': uid, 'name': name, 'cid': cid})
    form = RouteModelAddForm(data=request.POST)
    if form.is_valid():
        start = form.cleaned_data.get('begin_time')
        end = form.cleaned_data.get('end_time')
        ddl = form.cleaned_data.get('order_ddl')
        cc_id = form.cleaned_data.get('company')
        if end >= start >= ddl:
            form.save()
            return redirect('/company/' + str(uid) + '/route/list/')
        if end < start:
            form.add_error('end_time', '结束时间应不早于开始时间')
        if ddl > start:
            form.add_error('order_ddl', '最晚预定时间应早于开始时间')
        if cc_id != cid:
            form.add_error('company', '公司不可更改')
    return render(request, 'route_add.html', {'form': form, 'uid': uid, 'name': name, 'cid': cid})


def route_content(request, uid, rid):
    """路线详情"""
    row_object = models.RouteInfo.objects.filter(id=rid).first()
    name = models.UserInfo.objects.filter(id=uid).first().username
    content = row_object.content
    attention = row_object.attention
    tmp_list = content.split(';')
    content_list = []
    flag = 0
    for c in tmp_list:
        route_dict = {}
        if len(c.split(',')) == 1:
            flag = 1
            break
        date = c.split(',')[0]
        scene = c.split(',')[1]
        if not models.SceneInfo.objects.filter(scenic_name=scene).exists():
            flag = 2
            break
        sc_id = models.SceneInfo.objects.filter(scenic_name=scene).first().id
        route_dict['date'] = date
        route_dict['scene'] = scene
        route_dict['sc_id'] = sc_id
        content_list.append(route_dict)
    if flag == 0:
        return render(request, 'route_content.html',
                      {'attention': attention, 'content_list': content_list, 'uid': uid, 'name': name, 'rid': rid})
    else:
        return render(request, 'route_contenterror.html', {'uid': uid, 'name': name, 'rid': rid, 'flag': flag})


def route_scene(request, uid, sid):
    """路线景点详情"""
    row_obj = models.SceneInfo.objects.filter(id=sid).first()
    sname = row_obj.scenic_name
    name = models.UserInfo.objects.filter(id=uid).first().username
    return render(request, 'route_scene.html', {'row_obj': row_obj, 'name': name, 'uid': uid, 'sname': sname})


def route_sceneadd(request, uid, rid):
    """添加路线景点"""
    name = models.UserInfo.objects.filter(id=uid).first().username
    if request.method == "GET":
        return render(request, 'route_sceneadd.html', {'uid': uid, 'name': name, 'error': '', 'rid': rid})
        # 获取用户POST提交过来的数据
    date = request.POST.get('date')
    sc_name = request.POST.get('scene')
    ori_str = models.RouteInfo.objects.filter(id=rid).first().content
    add_str = ori_str + ';' + date + ',' + sc_name
    if models.SceneInfo.objects.filter(scenic_name=sc_name).exists():
        models.RouteInfo.objects.filter(id=rid).update(content=add_str)
        return redirect('/company/' + str(uid) + '/route/' + str(rid) + '/content/')
    else:
        error = '景点不存在'
        return render(request, 'route_sceneadd.html', {'uid': uid, 'name': name, 'error': error, 'rid': rid})


def book_list(request, uid):
    """预约列表"""
    row_obj = models.UserInfo.objects.filter(id=uid).first()
    name = row_obj.username
    cname = row_obj.company
    cid = cname.id
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict["content__contains"] = search_data
    queryset = models.OrderedRouteInfo.objects.filter(**data_dict).filter(company=cid)
    page_object = Pagination(request, queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    context = {"queryset": page_queryset,
               "search_data": search_data,
               "page_string": page_string,
               "uid": uid,
               "name": name,
               "cname": cname}
    return render(request, 'company_book_list.html', context)
