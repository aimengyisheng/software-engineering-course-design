from django.db import models


# Create your models here.
class UserInfo(models.Model):
    """用户信息表"""
    username = models.CharField(max_length=10, verbose_name="用户名", unique=True)
    password = models.CharField(max_length=1000, verbose_name="密码")
    phone_no = models.CharField(max_length=15, verbose_name="手机号")
    user_type_choices = ((1, '旅游者'), (2, '旅游局管理人员'), (3, '旅游公司管理人员'), (4, '系统管理员'))
    user_type = models.SmallIntegerField(choices=user_type_choices, verbose_name="用户类型")
    company = models.ForeignKey(to='CompanyInfo', to_field='company_name', blank=True, null=True,
                                on_delete=models.SET_NULL, verbose_name='用户所在公司')
    person_id = models.CharField(max_length=18, blank=True, null=True, verbose_name='身份证号')


class RouteInfo(models.Model):
    """旅游线路信息表"""
    begin_time = models.DateField(verbose_name='开始时间')
    end_time = models.DateField(verbose_name='结束时间')
    order_ddl = models.DateField(verbose_name='最晚预定时间')
    total_place = models.IntegerField(verbose_name='路线名额总数')
    remaining_place = models.IntegerField(verbose_name='剩余名额')
    route_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='线路价格')
    content = models.CharField(max_length=5000, verbose_name='线路详情')
    attention = models.CharField(max_length=5000, verbose_name='注意事项', blank=True, null=True)
    company = models.ForeignKey(to='CompanyInfo', to_field='id', on_delete=models.CASCADE, verbose_name='所属公司')


class SceneInfo(models.Model):
    """景点信息表"""
    scenic_name = models.CharField(max_length=30, verbose_name='景点名称')
    scenic_introduction = models.CharField(max_length=5000, verbose_name='景点介绍')
    scenic_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='门票价格')
    total_ticket = models.IntegerField(verbose_name='门票总数')
    remaining_ticket = models.IntegerField(verbose_name='剩余门票数')
    scenic_time = models.DateField(verbose_name='选择日期')


class HotelInfo(models.Model):
    """酒店信息表"""
    hotel_name = models.CharField(max_length=30, verbose_name='酒店名称')
    hotel_introduction = models.CharField(max_length=5000, verbose_name='酒店介绍')
    hotel_price = models.IntegerField(verbose_name='酒店价格')
    total_room = models.IntegerField(verbose_name='房间总数')
    remaining_room = models.IntegerField(verbose_name='剩余房间数')
    hotel_time = models.DateField(verbose_name='选择日期')


class OrderedSceneInfo(models.Model):
    """景点预约信息表"""
    username = models.ForeignKey(to='UserInfo', to_field='username', verbose_name='预约用户名', on_delete=models.CASCADE)
    scenic_id = models.ForeignKey(to='SceneInfo', to_field='id', verbose_name='预约景点编号', on_delete=models.CASCADE)
    ordered_time = models.DateField(verbose_name='预约日期')
    purchase_time = models.DateField(verbose_name='下单日期', auto_now=True)


class OrderedRouteInfo(models.Model):
    """路线预约信息表"""
    username = models.ForeignKey(to='UserInfo', to_field='username', verbose_name='预约用户名', on_delete=models.CASCADE)
    route_id = models.ForeignKey(to='RouteInfo', to_field='id', verbose_name='预约路线编号', on_delete=models.CASCADE)
    purchase_time = models.DateField(verbose_name='下单日期', auto_now=True)
    company = models.ForeignKey(to='CompanyInfo', to_field='id', on_delete=models.CASCADE, verbose_name='所属公司')


class TravelNewsInfo(models.Model):
    news_title = models.CharField(max_length=50, verbose_name='新闻标题')
    news_content = models.CharField(max_length=5000, verbose_name='新闻内容')
    news_date = models.DateField(verbose_name="新闻日期", auto_now=True)


class CompanyInfo(models.Model):
    """旅游公司信息表"""
    company_name = models.CharField(max_length=50, verbose_name="公司名称", unique=True)
