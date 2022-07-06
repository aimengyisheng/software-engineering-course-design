from django.core.exceptions import ValidationError
from django.db.models.functions import Concat
from django.shortcuts import render, redirect
import datetime
from app01 import models
from app01.utils.forms import TouristBRModelForm, NewsModelForm
from app01.utils.pagination import Pagination


def route_list(request, uid):
    """旅游线路列表"""
    row_obj = models.UserInfo.objects.filter(id=uid).first()
    name = row_obj.username
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict["content__contains"] = search_data
    queryset = models.RouteInfo.objects.filter(**data_dict)
    page_object = Pagination(request, queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    today = datetime.date.today()
    state = {}
    for item in queryset:
        if models.OrderedRouteInfo.objects.filter(route_id=item.id).filter(username=name).exists():
            state[item.id] = 1
        else:
            state[item.id] = 0
    context = {"queryset": page_queryset,
               "search_data": search_data,
               "page_string": page_string,
               "uid": uid,
               "name": name,
               "today": today,
               "state": state,
               }
    return render(request, 'tourist_route_list.html', context)


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
        return render(request, 'tourist_route_content.html',
                      {'attention': attention, 'content_list': content_list, 'uid': uid, 'name': name, 'rid': rid})
    else:
        return render(request, 'tourist_route_contenterror.html', {'uid': uid, 'name': name, 'rid': rid, 'flag': flag})


def scene_content(request, uid, sid):
    """景点详情"""
    row_obj = models.SceneInfo.objects.filter(id=sid).first()
    name = models.UserInfo.objects.filter(id=uid).first().username
    sname = row_obj.scenic_name
    intro = row_obj.scenic_introduction
    price = row_obj.scenic_price
    context = {'name': name, 'uid': uid, 'sid': sid, 'sname': sname, 'intro': intro, 'price': price}
    return render(request, 'tourist_scene_content.html', context)


def route_book(request, uid, rid):
    """预约路线"""
    row_obj = models.UserInfo.objects.filter(id=uid).first()
    route_obj = models.RouteInfo.objects.filter(id=rid).first()
    cname = route_obj.company
    tmp = models.OrderedRouteInfo.objects.create(username=row_obj, company=cname, route_id=route_obj)
    tmp.save()
    models.RouteInfo.objects.filter(id=rid).update(remaining_place=route_obj.remaining_place - 1)
    return redirect('/tourist/' + str(uid) + '/route/list/')


def route_cancel(request, uid, rid):
    """取消预约"""
    row_obj = models.UserInfo.objects.filter(id=uid).first()
    route_obj = models.RouteInfo.objects.filter(id=rid).first()
    cname = route_obj.company
    models.OrderedRouteInfo.objects.filter(username=row_obj, company=cname, route_id=route_obj).delete()
    models.RouteInfo.objects.filter(id=rid).update(remaining_place=route_obj.remaining_place + 1)
    return redirect('/tourist/' + str(uid) + '/route/list/')


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
    today = datetime.date.today()
    state = {}
    for item in queryset:
        if models.OrderedSceneInfo.objects.filter(scenic_id=item.id).filter(username=name).exists():
            state[item.id] = 1
        else:
            state[item.id] = 0
    context = {"queryset": page_queryset,
               "search_data": search_data,
               "page_string": page_string,
               "uid": uid,
               "name": name,
               'state': state,
               'today': today}
    return render(request, 'tourist_scene_list.html', context)


def scene_book(request, uid, sid):
    """预约景点"""
    row_obj = models.UserInfo.objects.filter(id=uid).first()
    scene_obj = models.SceneInfo.objects.filter(id=sid).first()
    tmp = models.OrderedSceneInfo.objects.create(username=row_obj, scenic_id=scene_obj,
                                                 ordered_time=scene_obj.scenic_time)
    tmp.save()
    models.SceneInfo.objects.filter(id=sid).update(remaining_ticket=scene_obj.remaining_ticket - 1)
    return redirect('/tourist/' + str(uid) + '/scene/list/')


def scene_cancel(request, uid, sid):
    """取消预约"""
    row_obj = models.UserInfo.objects.filter(id=uid).first()
    scene_obj = models.SceneInfo.objects.filter(id=sid).first()
    models.OrderedSceneInfo.objects.filter(username=row_obj, scenic_id=scene_obj).delete()
    models.SceneInfo.objects.filter(id=sid).update(remaining_ticket=scene_obj.remaining_ticket + 1)
    return redirect('/tourist/' + str(uid) + '/scene/list/')


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
    return render(request, 'tourist_news_list.html', context)


def news_content(request, uid, nid):
    """新闻详情"""
    row_obj = models.TravelNewsInfo.objects.filter(id=nid).first()
    name = models.UserInfo.objects.filter(id=uid).first().username
    context = {'name': name, 'uid': uid, 'nid': nid, 'row_obj': row_obj}
    return render(request, 'tourist_news_content.html', context)
