#coding=utf-8
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User, UserManager  
import django.utils.timezone as timezone
# Create your models here.

# 礼物
class Gift(models.Model):
	name = models.CharField(default='',verbose_name=u'名称',max_length=255) # 名称
	price = models.FloatField(verbose_name=u'礼物单价',default=0.0) # 礼物单价
	url = models.CharField(default='',verbose_name=u'礼物链接',max_length=255) # 礼物链接
	create_time = models.DateTimeField(verbose_name=u'创建时间',default=timezone.now)
	update_time = models.DateTimeField(verbose_name=u'修改时间',default=timezone.now,auto_now=True)	

# 充值项目
class Item(models.Model):
	money = models.FloatField(verbose_name=u'金额',default=0.0) # 充值金额
	momentMoney = models.FloatField(verbose_name=u'虚拟金额',default=0.0) # 虚拟金额
	note = models.CharField(default='',verbose_name=u'名称',max_length=255) # 描述
	IAPId = models.CharField(blank=True,null=True,verbose_name=u'IAPId',max_length=255) # IAPId

# 充值历史
class RechargeHistory(models.Model):
	user = models.ForeignKey(User,verbose_name=u'对应用户',blank=True,null=True) # 对应用户	
	item = models.ForeignKey(Item,verbose_name=u'对应项目',blank=True,null=True) # 对应项目

# 用户
class User(models.Model):
	auth_type = models.CharField(default='',verbose_name=u'第三方账号类型',max_length=255) # 	第三方账号类型
	third_party_id = models.CharField(default='',verbose_name=u'第三方标识',max_length=255) # 	第三方标识
	name = models.CharField(default='',verbose_name=u'昵称',max_length=255) # 昵称
	sex = models.IntegerField(verbose_name=u'性别',default=1) # 性别 1-男 2-女
	avatar = models.CharField(default='',verbose_name=u'头像',max_length=255) # 头像
	city = models.CharField(default='',verbose_name=u'城市',max_length=255) # 城市
	# device_tag = models.CharField(default='',verbose_name=u'设备号',max_length=255) # 设备号
	create_time = models.DateTimeField(verbose_name=u'创建时间',default=timezone.now)
	update_time = models.DateTimeField(verbose_name=u'修改时间',default=timezone.now,auto_now=True)	

# 设备信息
class DeviceInfo(models.Model):
	user = models.ForeignKey(User,verbose_name=u'对应host用户',blank=True,null=True) # 对应用户	
	client_type = models.CharField(default='',verbose_name=u'客户端类型',max_length=255) # 客户端类型
	version = models.CharField(default='',verbose_name=u'客户端版本',max_length=255) # 客户端版本
	os_version = models.CharField(default='',verbose_name=u'客户端系统版本',max_length=255) # 客户端系统版本
	platform = models.CharField(default='',verbose_name=u'应用的发布平台',max_length=255) # 应用的发布平台
	device_identifier = models.CharField(default='',verbose_name=u'设备号',max_length=255) # 设备号
	machine_type = models.CharField(default='',verbose_name=u'设备型号',max_length=255) # 设备型号
	idfa = models.CharField(blank=True,null=True,verbose_name=u'iOS idfa',max_length=255) # iOS idfa
	device_token = models.CharField(blank=True,null=True,verbose_name=u'iOS推送设备号',max_length=255) # iOS推送设备号
	push_type = models.IntegerField(verbose_name=u'iOS推送证书类型',blank=True,null=True) # iOS推送证书类型
	xiaomi_push = models.CharField(blank=True,null=True,verbose_name=u'小米推送设备号',max_length=255) # 小米推送设备号
	huawei_push = models.CharField(blank=True,null=True,verbose_name=u'华为推送设备号',max_length=255) # 华为推送设备号

# 账户
class Account(models.Model):
	user = models.ForeignKey(User,verbose_name=u'对应用户',blank=True,null=True) # 对应用户
	amount = models.FloatField(verbose_name=u'账户余额',default=0.0) # 账户余额
	create_time = models.DateTimeField(verbose_name=u'创建时间',default=timezone.now)
	update_time = models.DateTimeField(verbose_name=u'修改时间',default=timezone.now,auto_now=True)	

# 频道
class Channel(models.Model):
	channel_id = models.IntegerField(verbose_name=u'频道ID',default=0) # 频道ID（腾讯云识别的ID）
	user = models.ForeignKey(User,verbose_name=u'对应host用户',blank=True,null=True) # 对应用户	
	title = models.CharField(default='',verbose_name=u'频道标题',max_length=255) # 频道标题
	cover = models.CharField(default='',verbose_name=u'频道封面',max_length=255) # 频道封面
	audience_num = models.IntegerField(default=0,verbose_name=u'当前频道观看人数') # 当前频道观看人数
	channel_status = models.IntegerField(default=0,verbose_name=u'频道状态') # 频道状态
	last_access_time = models.DateTimeField(verbose_name=u'最近一次访问时间',default=timezone.now) # 最近一次访问时间
	create_time = models.DateTimeField(verbose_name=u'创建时间',default=timezone.now)
	update_time = models.DateTimeField(verbose_name=u'修改时间',default=timezone.now,auto_now=True)	

# 喊麦信息(交互)
class Interact(models.Model):
	channel = models.ForeignKey(Channel,verbose_name=u'对应频道',related_name='interact_channel',blank=True,null=True) # 对应频道
	user = models.ForeignKey(User,verbose_name=u'对应用户',related_name='interact_user',blank=True,null=True) # 对应用户
	position = models.IntegerField(verbose_name=u'话麦位置',default=0) # 话麦位置
	create_time = models.DateTimeField(verbose_name=u'创建时间',default=timezone.now)
	update_time = models.DateTimeField(verbose_name=u'修改时间',default=timezone.now,auto_now=True)	

# 用户收看频道记录
class UserChannelRecord(models.Model):
	channel = models.ForeignKey(Channel,verbose_name=u'对应频道',blank=True,null=True) # 对应频道
	user = models.ForeignKey(User,verbose_name=u'对应用户',blank=True,null=True) # 对应用户	
	#position = models.IntegerField(verbose_name=u'位置',default=0) # 位置
	status = models.IntegerField(verbose_name=u'收看频道状态',default=1) # 0-已离开 1-在收看
	create_time = models.DateTimeField(verbose_name=u'创建时间',default=timezone.now)
	update_time = models.DateTimeField(verbose_name=u'修改时间',default=timezone.now,auto_now=True)	

# 送礼记录
class GiftRecord(models.Model):
	gift = models.ForeignKey(Gift,verbose_name=u'对应礼物',related_name='gc_gift',blank=True,null=True) # 关联的礼物
	from_user = models.ForeignKey(User,verbose_name=u'送礼用户',related_name='from_user',blank=True,null=True) # 送礼用户
	to_user = models.ForeignKey(User,verbose_name=u'收礼用户',related_name='to_user',blank=True,null=True) # 收礼用户
	number = models.IntegerField(verbose_name=u'送礼数量',default=1) # 送礼数量
	price = models.FloatField(verbose_name=u'送礼钱数',default=0.0) # 送礼钱数
	create_time = models.DateTimeField(verbose_name=u'创建时间',default=timezone.now)
	update_time = models.DateTimeField(verbose_name=u'修改时间',default=timezone.now,auto_now=True)	

# 腾讯云用户信息
class TencentCloudUsreInfo(models.Model):
	user = models.ForeignKey(User,verbose_name=u'对应用户',blank=True,null=True) # 用户
	user_tencent_id = models.CharField(default='',verbose_name=u'用户腾讯云ID',max_length=255) # 用户腾讯云ID
	user_sig = models.CharField(default='',verbose_name=u'腾讯云用户签名',max_length=5000) # 腾讯云用户签名
	tim_id = models.CharField(default='',verbose_name=u'腾讯云用户标识',max_length=255) # 腾讯云用户标识
	create_time = models.DateTimeField(verbose_name=u'创建时间',default=timezone.now)
	update_time = models.DateTimeField(verbose_name=u'修改时间',default=timezone.now,auto_now=True)	


# class Emoji(models.Model):
# 	name = models.CharField(default='',verbose_name=u'名称',max_length=255) # 名称