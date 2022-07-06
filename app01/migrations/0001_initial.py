# Generated by Django 4.0.5 on 2022-07-06 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=50, unique=True, verbose_name='公司名称')),
            ],
        ),
        migrations.CreateModel(
            name='HotelInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_name', models.CharField(max_length=30, verbose_name='酒店名称')),
                ('hotel_introduction', models.CharField(max_length=5000, verbose_name='酒店介绍')),
                ('hotel_price', models.IntegerField(verbose_name='酒店价格')),
                ('total_room', models.IntegerField(verbose_name='房间总数')),
                ('remaining_room', models.IntegerField(verbose_name='剩余房间数')),
                ('hotel_time', models.DateField(verbose_name='选择日期')),
            ],
        ),
        migrations.CreateModel(
            name='SceneInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scenic_name', models.CharField(max_length=30, verbose_name='景点名称')),
                ('scenic_introduction', models.CharField(max_length=5000, verbose_name='景点介绍')),
                ('scenic_price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='门票价格')),
                ('total_ticket', models.IntegerField(verbose_name='门票总数')),
                ('remaining_ticket', models.IntegerField(verbose_name='剩余门票数')),
                ('scenic_time', models.DateField(verbose_name='选择日期')),
            ],
        ),
        migrations.CreateModel(
            name='TravelNewsInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_title', models.CharField(max_length=50, verbose_name='新闻标题')),
                ('news_content', models.CharField(max_length=5000, verbose_name='新闻内容')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=10, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=1000, verbose_name='密码')),
                ('phone_no', models.CharField(max_length=15, verbose_name='手机号')),
                ('user_type', models.SmallIntegerField(choices=[(1, '旅游者'), (2, '旅游局管理人员'), (3, '旅游公司管理人员'), (4, '系统管理员')], verbose_name='用户类型')),
                ('person_id', models.CharField(blank=True, max_length=18, null=True, verbose_name='身份证号')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app01.companyinfo', to_field='company_name', verbose_name='用户所在公司')),
            ],
        ),
        migrations.CreateModel(
            name='RouteInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin_time', models.DateField(verbose_name='开始时间')),
                ('end_time', models.DateField(verbose_name='结束时间')),
                ('order_ddl', models.DateField(verbose_name='最晚预定时间')),
                ('total_place', models.IntegerField(verbose_name='路线名额总数')),
                ('remaining_place', models.IntegerField(verbose_name='剩余名额')),
                ('route_price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='线路价格')),
                ('content', models.CharField(max_length=5000, verbose_name='线路详情')),
                ('attention', models.CharField(blank=True, max_length=5000, null=True, verbose_name='注意事项')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.companyinfo', verbose_name='所属公司')),
            ],
        ),
        migrations.CreateModel(
            name='OrderedSceneInfo',
            fields=[
                ('ordered_scene_id', models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='景点预约信息编号')),
                ('ordered_time', models.DateField(verbose_name='预约日期')),
                ('purchase_time', models.DateField(auto_now=True, verbose_name='下单日期')),
                ('scenic_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.sceneinfo', verbose_name='预约景点编号')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.userinfo', to_field='username', verbose_name='预约用户名')),
            ],
        ),
        migrations.CreateModel(
            name='OrderedRouteInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_time', models.DateField(auto_now=True, verbose_name='下单日期')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.companyinfo', verbose_name='所属公司')),
                ('route_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.routeinfo', verbose_name='预约路线编号')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.userinfo', to_field='username', verbose_name='预约用户名')),
            ],
        ),
    ]