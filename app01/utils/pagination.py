"""
自定义的分页组件
在视图函数中：
    def user_list(request):
        1. 根据情况筛选数据
        queryset=models.Userinfo.objects.all()
        2. 实例化分页图像
        page_object=Pagination(request,queryset)

        context={
            'queryset': page_object.page_queryset, #分完页的数据
            'page_string': page_object.html()      #生成页码

在HTML页面中：
    {% for obj in queryset %}
        {{obj.xx}}
    {% endfor %}

    <ul class="pagination">
        <li class="disabled"><a href="#" aria-label="Previous"><span aria-hidden="true"><<</span></a></li>
            {{ page_string }}
        <li><a href="#" aria-label="Next"><span aria-hidden="true">>></span></a></li>
    </ul>
"""
from django.utils.safestring import mark_safe


class Pagination(object):
    def __init__(self, request, queryset, page_size=10, page_param="page", page_range=5):
        '''
        :param request: 请求的对象
        :param queryset: 符合条件的数据
        :param page_size: 每页显示多少条数据
        :param page_param: 在url中传递的获取分页的参数
        :param page_range: 显示页数范围
        '''
        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        self.page_range = page_range
        self.page_param = page_param
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset = queryset[self.start:self.end]
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count

    def html(self):
        page_strlist = []
        self.query_dict.setlist(self.page_param, [1])
        start_page = max(self.page - self.page_range, 1)
        end_page = min(self.total_page_count + 1, self.page + self.page_range + 1)
        first = '<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode())
        self.query_dict.setlist(self.page_param, [max(1, self.page - 1)])
        prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_strlist.append(first)
        page_strlist.append(prev)
        for i in range(start_page, end_page):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_strlist.append(ele)
        self.query_dict.setlist(self.page_param, [min(self.page + 1, self.total_page_count)])
        nxt = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        end = first = '<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode())
        search = '''<li>
                <form style="float: left;margin-left: -1px" method="get">
                    <input name="page"
                           style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0;"
                           type="text" class="form-control" placeholder="页码">
                    <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
                </form>
            </li>'''
        page_strlist.append(nxt)
        page_strlist.append(end)
        page_strlist.append(search)
        page_string = mark_safe("".join(page_strlist))
        return page_string
