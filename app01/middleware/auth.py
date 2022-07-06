from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        # 0.排除那些不需要登录就能访问的页面
        if request.path_info in ['/login/', '/image/code/', '/register/']:
            return
        # 1.读取当前访问的用户的session信息，如果能读到，说明登陆过，可以向后走
        info_dict = request.session.get('info')
        if info_dict:
            return
        # 2. 没有登录过，重新回到登录页面
        return redirect('/login/')
