#coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'maomen.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/see_me','broadcast.views.see_me'),
    url(r'^a/','broadcast.views.a'),

    # 账户相关
    url(r'^auth/third_party','broadcast.views.third_party'),
    url(r'^auth/refresh_userSig','broadcast.views.refresh_userSig'),

    # 礼物
    url(r'^gift/list','broadcast.views.gift_list'),

    # 用户信息
    url(r'^user/profile','broadcast.views.other_profile'),
    url(r'^user/self_profile','broadcast.views.self_profile'),
    url(r'^user/update','broadcast.views.user_update'),
    
    # 频道相关
    url(r'^channel/create','broadcast.views.create_channel'),
    url(r'^channel/close','broadcast.views.close_channel'),
    url(r'^channel/channel_id','broadcast.views.get_next_broadcast_channel'),
    url(r'^channel/audience_num','broadcast.views.get_audience_num'),
    url(r'^channel/list','broadcast.views.get_channel_list'),
    url(r'^channel/interact/add','broadcast.views.add_channel_interact'),
    url(r'^channel/interact/delete','broadcast.views.delete_channel_interact'),
    url(r'^channel/user/add','broadcast.views.add_channel_view_user'),
    url(r'^channel/user/delete','broadcast.views.delete_channel_view_user'),
    url(r'^channel/user/list','broadcast.views.channel_user_list'),
    

    # sign
    url(r'^log_serv/fetch_cos_sign','broadcast.views.fetch_cos_sign'),
    
    
)	
