from django.core.exceptions import ValidationError
from django.db.models.functions import Concat
from django.shortcuts import render, redirect

from app01 import models
from app01.utils.forms import UserModelForm, SceneModelForm, NewsModelForm
from app01.utils.pagination import Pagination


def scene_list(request, uid):
    """旅游景点列表"""
    row_obj = models.UserInfo.objects.filter(id=uid).first()
    name = row_obj.username
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict["scenic_name__contains"] = search_data
    queryset = models.SceneInfo.objects.filter(**data_dict)
    page_object = Pagination(request, queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    context = {"queryset": page_queryset,
               "search_data": search_data,
               "page_string": page_string,
               "uid": uid,
               "name": name}
    return render(request, 'scene_list.html', context)


def scene_delete(request, uid, sid):
    """删除景点"""
    models.SceneInfo.objects.filter(id=sid).delete()
    return redirect('/auth/' + str(uid) + '/scene/list/')


def scene_edit(request, uid, sid):
    """编辑景点"""
    row_object = models.SceneInfo.objects.filter(id=sid).first()
    name = models.UserInfo.objects.filter(id=uid).first().username
    sname = row_object.scenic_name
    if request.method == "GET":
        # 根据id去数据库获取要编辑的数据
        form = SceneModelForm(instance=row_object)
        return render(request, 'scene_edit.html', {'form': form, 'uid': uid, 'name': name})
    form = SceneModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()  # 保存的是用户输入的所有数据
        intro = form.cleaned_data.get('scenic_introduction')
        query_set = models.SceneInfo.objects.filter(scenic_name=sname)
        for item in query_set:
            item.scenic_introduction = intro
        models.SceneInfo.objects.bulk_update(query_set, ['scenic_introduction'])
        return redirect('/auth/' + str(uid) + '/scene/list/')
    return render(request, 'scene_edit.html', {'form': form, 'uid': uid, 'name': name})


def scene_content(request, uid, sid):
    """景点详情"""
    row_obj = models.SceneInfo.objects.filter(id=sid).first()
    name = models.UserInfo.objects.filter(id=uid).first().username
    sname = row_obj.scenic_name
    intro = row_obj.scenic_introduction
    context = {'name': name, 'uid': uid, 'sid': sid, 'sname': sname, 'intro': intro}
    return render(request, 'scene_content.html', context)


def scene_add(request, uid):
    """添加景点"""
    row_obj = models.UserInfo.objects.filter(id=uid).first()
    name = row_obj.username
    if request.method == "GET":
        form = SceneModelForm()
        return render(request, 'scene_add.html', {"form": form, 'uid': uid, 'name': name})
    form = SceneModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/auth/' + str(uid) + '/scene/list/')
    return render(request, 'scene_add.html', {'form': form, 'uid': uid, 'name': name})


def scene_multi_add(request, uid):
    """添加路线景点"""
    name = models.UserInfo.objects.filter(id=uid).first().username
    if request.method == "GET":
        return render(request, 'scene_multi_add.html', {'uid': uid, 'name': name})
        # 获取用户POST提交过来的数据
    sc_name = request.POST.get('sc_name')
    multi_date = request.POST.get('multi_date')
    price = request.POST.get('price')
    if not models.SceneInfo.objects.filter(scenic_name=sc_name).exists():
        return render(request, 'scene_multi_add.html', {'uid': uid, 'name': name, 'error1': '景点不存在'})
    elif len(multi_date) != 10 and (len(multi_date) + 1) % 11 != 0:
        return render(request, 'scene_multi_add.html',
                      {'uid': uid, 'name': name, 'error2': '日期格式错误，请确保每个日期都为10位，且无多余分号'})
    row_obj = models.SceneInfo.objects.filter(scenic_name=sc_name).first()
    date_list = multi_date.split(';')
    content = {
        'scenic_name': sc_name,
        'scenic_introduction': row_obj.scenic_introduction,
        'scenic_price': price,
        'total_ticket': row_obj.total_ticket,
        'remaining_ticket': row_obj.remaining_ticket
    }
    for date in date_list:
        content['scenic_time'] = date
        tmp = models.SceneInfo.objects.create(**content)
        tmp.save()
    return redirect('/auth/' + str(uid) + '/scene/list/')


def news_list(request, uid):
    """旅游新闻列表"""
    row_obj = models.UserInfo.objects.filter(id=uid).first()
    name = row_obj.username
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict["news_title__contains"] = search_data
    queryset = models.TravelNewsInfo.objects.filter(**data_dict)
    page_object = Pagination(request, queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    context = {"queryset": page_queryset,
               "search_data": search_data,
               "page_string": page_string,
               "uid": uid,
               "name": name}
    return render(request, 'news_list.html', context)


def news_delete(request, uid, nid):
    """删除新闻"""
    models.TravelNewsInfo.objects.filter(id=nid).delete()
    return redirect('/auth/' + str(uid) + '/news/list/')


def news_edit(request, uid, nid):
    """编辑新闻"""
    row_object = models.TravelNewsInfo.objects.filter(id=nid).first()
    name = models.UserInfo.objects.filter(id=uid).first().username
    if request.method == "GET":
        # 根据id去数据库获取要编辑的数据
        form = NewsModelForm(instance=row_object)
        return render(request, 'news_edit.html', {'form': form, 'uid': uid, 'name': name})
    form = NewsModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()  # 保存的是用户输入的所有数据
        return redirect('/auth/' + str(uid) + '/news/list/')
    return render(request, 'news_edit.html', {'form': form, 'uid': uid, 'name': name})


def news_content(request, uid, nid):
    """新闻详情"""
    row_obj = models.TravelNewsInfo.objects.filter(id=nid).first()
    name = models.UserInfo.objects.filter(id=uid).first().username
    context = {'name': name, 'uid': uid, 'nid': nid, 'row_obj': row_obj}
    return render(request, 'news_content.html', context)


def news_add(request, uid):
    """添加新闻"""
    row_obj = models.UserInfo.objects.filter(id=uid).first()
    name = row_obj.username
    if request.method == "GET":
        form = NewsModelForm()
        return render(request, 'news_add.html', {"form": form, 'uid': uid, 'name': name})
    form = NewsModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/auth/' + str(uid) + '/news/list/')
    return render(request, 'news_add.html', {'form': form, 'uid': uid, 'name': name})


def book_list(request, uid):
    """预约列表"""
    row_obj = models.UserInfo.objects.filter(id=uid).first()
    name = row_obj.username
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict["scenic_name__contains"] = search_data
    queryset = models.OrderedSceneInfo.objects.filter(**data_dict)
    page_object = Pagination(request, queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    context = {"queryset": page_queryset,
               "search_data": search_data,
               "page_string": page_string,
               "uid": uid,
               "name": name
               }
    return render(request, 'auth_book_list.html', context)
