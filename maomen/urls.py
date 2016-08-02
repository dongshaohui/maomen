#coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'maomen.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # 账户相关
    url(r'^auth/third_party','broadcast.views.third_party'),
    url(r'^auth/refresh_userSig','broadcast.views.refresh_userSig'),

    # 礼物
    url(r'^gift/list','broadcast.views.gift_list'),
    url(r'^gift/send','broadcast.views.send_gift'),

    # 用户信息
    url(r'^user/profile','broadcast.views.other_profile'),
    url(r'^user/self_profile','broadcast.views.self_profile'),
    url(r'^user/update','broadcast.views.user_update'),
    
    # 频道相关
    url(r'^channel/create','broadcast.views.create_channel'),
    url(r'^channel/close','broadcast.views.close_channel'),
    url(r'^channel/channel_id','broadcast.views.get_next_broadcast_channel'),
    url(r'^channel/info','broadcast.views.get_channel_info'),
    url(r'^channel/audience_num','broadcast.views.get_audience_num'),
    url(r'^channel/list','broadcast.views.get_channel_list'),
    url(r'^channel/interact/add','broadcast.views.add_channel_interact'),
    url(r'^channel/interact/delete','broadcast.views.delete_channel_interact'),
    url(r'^channel/user/add','broadcast.views.add_channel_view_user'),
    url(r'^channel/user/delete','broadcast.views.delete_channel_view_user'),
    url(r'^channel/user/list','broadcast.views.channel_user_list'),
    
    # 应用类
    url(r'^app/minimize_start','broadcast.views.minimize_start'),
    url(r'^app/update_device_token','broadcast.views.update_device_token'),
   	url(r'^app/xiaomi_message_push','broadcast.views.xiaomi_message_push'), # 小米推送
   	url(r'^app/ios_push/upush_message','broadcast.views.upush_message'), # 友盟推送
   	url(r'^wallet/validate_receipt','broadcast.views.validate_receipt'), # ios验证凭证
    # 客户端轮训
    url(r'^channel/client/round_check','broadcast.views.round_check'),
    # sign
    url(r'^log_serv/fetch_cos_sign','broadcast.views.fetch_cos_sign'),
    
	# url(r'^emoji_test','broadcast.views.emoji_test'),    
)	
