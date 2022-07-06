"""p2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01.views import company, user, account, auth, tourist

urlpatterns = [
    # path('admin/', admin.site.urls),
    # 登录
    path('register/', account.register),
    path('login/', account.login),
    path('logout/', account.logout),
    path('image/code/', account.image_code),
    # 用户主页
    path('home/<int:uid>/', user.home),
    path('user/<int:uid>/info/', user.info),
    path('user/<int:uid>/password/reset/', user.password_reset),
    path('company/<int:uid>/', company.home),
    # 旅游公司信息管理
    path('company/<int:uid>/route/list/', company.route_list),
    path('company/<int:uid>/route/<int:rid>/edit/', company.route_edit),
    path('company/<int:uid>/route/<int:rid>/delete/', company.route_delete),
    path('company/<int:uid>/route/add/', company.route_add),
    path('company/<int:uid>/route/<int:rid>/content/', company.route_content),
    path('company/<int:uid>/route/<int:sid>/scene/', company.route_scene),
    path('company/<int:uid>/route/<int:rid>/scene/add', company.route_sceneadd),
    path('company/<int:uid>/book/list/', company.book_list),
    # path('company/<int:cid>/hotel/list/', company.hotel_list),
    # path('company/<int:cid>/hotel/edit/', company.hotel_edit),
    # path('company/<int:cid>/hotel/delete/', company.hotel_delete),
    # 旅游局信息管理
    path('auth/<int:uid>/scene/list/', auth.scene_list),
    path('auth/<int:uid>/scene/<int:sid>/edit/', auth.scene_edit),
    path('auth/<int:uid>/scene/<int:sid>/delete/', auth.scene_delete),
    path('auth/<int:uid>/scene/<int:sid>/content/', auth.scene_content),
    path('auth/<int:uid>/scene/add/', auth.scene_add),
    path('auth/<int:uid>/scene/multi_add/', auth.scene_multi_add),
    path('auth/<int:uid>/news/list/', auth.news_list),
    path('auth/<int:uid>/news/<int:nid>/edit/', auth.news_edit),
    path('auth/<int:uid>/news/<int:nid>/delete/', auth.news_delete),
    path('auth/<int:uid>/news/<int:nid>/content/', auth.news_content),
    path('auth/<int:uid>/news/add/', auth.news_add),
    path('auth/<int:uid>/book/list/', auth.book_list),
    # 旅游者管理
    path('tourist/<int:uid>/route/list/', tourist.route_list),
    path('tourist/<int:uid>/route/<int:rid>/content/', tourist.route_content),
    path('tourist/<int:uid>/scene/<int:sid>/content/', tourist.scene_content),
    path('tourist/<int:uid>/route/<int:rid>/book/', tourist.route_book),
    path('tourist/<int:uid>/route/<int:rid>/cancel/', tourist.route_cancel),
    path('tourist/<int:uid>/scene/list/', tourist.scene_list),
    path('tourist/<int:uid>/scene/<int:sid>/book/', tourist.scene_book),
    path('tourist/<int:uid>/scene/<int:sid>/cancel/', tourist.scene_cancel),
    path('tourist/<int:uid>/news/list/', tourist.news_list),
    path('tourist/<int:uid>/news/<int:nid>/content/', tourist.news_content),
]
