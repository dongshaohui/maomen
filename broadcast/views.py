#coding=utf-8
from django.shortcuts import render
from broadcast.models import *
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.template.defaulttags import register
from django.db import transaction
from broadcast_conf import WxPayConf_pub
import base64
import zlib
import json
import time
import os,sys,commands
import random
import hmac
import hashlib,urllib2,requests
import binascii
import datetime
import base64
import re
# Create your views here.

def get_user_sig(user_id):
	sig_user_id = WxPayConf_pub.USER_SIG_PREFIX + str(user_id)
	current_path = os.getcwd()
	sig_record_file_name = "sig_record_file_%s" % sig_user_id
	commands.getoutput("rm -rf %s" % sig_record_file_name)
	comds = current_path+"/tls_licence_tools gen ec_key.pem %s %d %s" % (sig_record_file_name,WxPayConf_pub.SDK_APPID,sig_user_id)
	# print comds
	commands.getoutput(current_path+"/tls_licence_tools gen ec_key.pem %s %d %s" % (sig_record_file_name,WxPayConf_pub.SDK_APPID,sig_user_id))
	result = commands.getoutput("cat %s" % sig_record_file_name )
	commands.getoutput("rm -rf %s" % sig_record_file_name)
	return result

###########################################
#
# 	账户相关
#
###########################################

@csrf_exempt
def third_party(request):
	response = {}
	auth_type = None
	third_party_id = None
	name = None
	sex = None
	avatar = None
	city = None

	received_json_data = json.loads(request.body)
	auth_type = received_json_data['auth_type']
	third_party_id = received_json_data['third_party_id']
	name = received_json_data['name']
	sex = received_json_data['sex']
	avatar = received_json_data['avatar']
	city = received_json_data['city']
	# city = received_json_data['city']

	# re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
	# name = re_pattern.sub(u'\uFFFD', name)

	users = User.objects.filter(third_party_id=third_party_id)
	new_user = None
	new_tim_id = None
	new_user_sig_id = None
	new_user_sig = None
	if len(users) > 0:
		new_user = users[0]
		new_tim_id = TencentCloudUsreInfo.objects.get(user=new_user).tim_id
		new_user_sig_id = WxPayConf_pub.USER_SIG_PREFIX + (str)(new_user.id)
		new_user_sig = TencentCloudUsreInfo.objects.get(user=new_user).user_sig
	else:
		# 创建新用户
		new_user = User.objects.create(auth_type=auth_type,third_party_id=third_party_id,
			name=name,sex=sex,avatar=avatar,city=city)

		new_account = Account.objects.create(user=new_user)

		# 创建新频道
		new_channel = Channel.objects.create(user=new_user)
		new_channel.channel_id = new_channel.id + WxPayConf_pub.RESERVED_CHANNEL_NUMBER
		new_channel.save()

		new_user_sig_id = WxPayConf_pub.USER_SIG_PREFIX + (str)(new_user.id)
		new_user_sig = get_user_sig(new_user.id)
		new_tim_id = WxPayConf_pub.TIM_PREFIX + (str)(new_user.id)
		new_tencent_user_info = TencentCloudUsreInfo.objects.create(user=new_user,
			user_tencent_id=new_user_sig_id,user_sig=new_user_sig,tim_id=new_tim_id)

	response['status'] = 0
	response['message'] = 'OK'
	response['data'] = {}
	response['data']['user_id'] = new_user.id
	response['data']['user_sig_id'] = new_user_sig_id
	response['data']['user_sig'] = new_user_sig
	response['data']['tim_id'] = new_tim_id
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")

# 刷新user_sig
@csrf_exempt
def refresh_userSig(request):
	response = {}
	user_id = None
	if 'user_id' in request.POST:
		user_id = int(request.POST['user_id'])
	else:
		user_id = int(request.GET['user_id'])

	current_user = User.objects.get(id=user_id)
	user_sig = get_user_sig(current_user.id)

	ten_cent_user_info = TencentCloudUsreInfo.objects.get(user=current_user)
	ten_cent_user_info.user_sig = user_sig
	ten_cent_user_info.save()

	response['status'] = 0
	response['message'] = 'OK'
	response['data'] = {}	
	response['data']['user_sig'] = user_sig
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")

###########################################
#
# 	礼物相关
#
###########################################

@csrf_exempt
def gift_list(request):
	response = {}
	response['status'] = 0
	response['message'] = 'OK'
	response['data'] = []

	all_gifts = Gift.objects.all()
	for gift in all_gifts:
		temp_gift_record = {}
		temp_gift_record['price'] = gift.price
		temp_gift_record['gift_id'] = gift.id
		temp_gift_record['icon_url'] = gift.url
		temp_gift_record['name'] = gift.name
		response['data'].append(temp_gift_record)

	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")

@csrf_exempt
def send_gift(request):
	response = {}

	from_user = None
	to_user = None
	gift_id = None
	num = 1
	if 'from_user' in request.POST:
		from_user = int(request.POST['from_user'])
	else:
		from_user = int(request.GET['from_user'])

	if 'to_user' in request.POST:
		to_user = int(request.POST['to_user'])
	else:
		to_user = int(request.GET['to_user'])

	if 'gift_id' in request.POST:
		gift_id = int(request.POST['gift_id'])
	else:
		gift_id = int(request.GET['gift_id'])

	if 'num' in request.POST:
		num = int(request.POST['num'])
	elif 'num' in request.GET:
		num = int(request.GET['num'])

	current_gift = Gift.objects.get(id=gift_id)
	current_from_user = User.objects.get(id=from_user)
	current_to_user = User.objects.get(id=to_user)
	current_from_account = Account.objects.get(user=current_from_user)
	
	current_from_account.amount = current_from_account.amount - current_gift.price * (float)(num)
	current_from_account.save()

	gift_record = GiftRecord.objects.create(gift=current_gift,from_user=current_from_user,
		to_user=current_to_user,number=num,price=current_gift.price * (float)(num))

	response['status'] = 0
	response['message'] = 'OK'
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")

###########################################
#
# 	用户信息
#
###########################################

# 获取他人的个人信息
@csrf_exempt
def other_profile(request):
	response = {}
	target_user_id = None
	if 'target_user_id' in request.GET:
		target_user_id = int(request.GET['target_user_id'])
	elif 'target_user_id' in request.POST:
		target_user_id = int(request.POST['target_user_id'])

	current_user = User.objects.get(id=target_user_id)

	received_gift_price = 0.0 # 收到礼物的数量
	recieved_gift_records = GiftRecord.objects.filter(to_user=current_user)
	for recieved_gift_record in recieved_gift_records:
		received_gift_price += (float)(recieved_gift_record.price)

	sent_gift_price = 0.0 # 送出礼物的数量
	sent_gift_records = GiftRecord.objects.filter(from_user=current_user)
	for sent_gift_record in sent_gift_records:
		sent_gift_price += (float)(sent_gift_record.price)

	response['status'] = 0
	response['message'] = 'OK'	
	response['data'] = {}
	response['data']['avatar'] = current_user.avatar
	response['data']['city'] = current_user.city
	response['data']['received_gift_num'] = int(received_gift_price)
	response['data']['sent_gift_num'] = int(sent_gift_price)
	response['data']['user_id'] = current_user.id
	response['data']['sex'] = current_user.sex
	response['data']['name'] = current_user.name
	response['data']['tim_id'] = TencentCloudUsreInfo.objects.get(user=current_user).tim_id
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")

@csrf_exempt
def self_profile(request):
	response = {}
	user_id = None
	if 'user_id' in request.GET:
		user_id = int(request.GET['user_id'])
	elif 'user_id' in request.POST:
		user_id = int(request.POST['user_id'])

	current_user = User.objects.get(id=user_id)

	received_gift_price = 0.0 # 收到礼物的数量
	recieved_gift_records = GiftRecord.objects.filter(to_user=current_user)
	for recieved_gift_record in recieved_gift_records:
		received_gift_price += (float)(recieved_gift_record.price)

	sent_gift_price = 0.0 # 送出礼物的数量
	sent_gift_records = GiftRecord.objects.filter(from_user=current_user)
	for sent_gift_record in sent_gift_records:
		sent_gift_price += (float)(sent_gift_record.price)

	response['status'] = 0
	response['message'] = 'OK'	
	response['data'] = {}
	response['data']['user'] = {}
	response['data']['user']['avatar'] = current_user.avatar
	response['data']['user']['city'] = current_user.city
	response['data']['user']['received_gift_num'] = int(received_gift_price)
	response['data']['user']['sent_gift_num'] = int(sent_gift_price)
	response['data']['user']['user_id'] = current_user.id
	response['data']['user']['sex'] = current_user.sex
	response['data']['user']['name'] = current_user.name
	response['data']['user']['tim_id'] = TencentCloudUsreInfo.objects.get(user=current_user).tim_id
	response['data']['account'] = Account.objects.get(user=current_user).amount
	response['data']['account_verson'] = 10 # ?????
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")	

@csrf_exempt
def user_update(request):
	response = {}
	user_id = None
	name = None
	avatar = None
	sex = None
	city = None
	received_json_data = json.loads(request.body)

	user_id = received_json_data['user_id']
	name = received_json_data['name']
	avatar = received_json_data['avatar']
	sex = received_json_data['sex']
	city = received_json_data['city']

	# if 'user_id' in request.GET:
	# 	user_id = int(request.GET['user_id'])
	# elif 'user_id' in request.POST:
	# 	user_id = int(request.POST['user_id'])

	# if 'name' in request.GET:
	# 	name = request.GET['name']
	# elif 'name' in request.POST:
	# 	name = request.POST['name']

	# if 'avatar' in request.GET:
	# 	avatar = request.GET['avatar']
	# elif 'avatar' in request.POST:
	# 	avatar = request.POST['avatar']

	# if 'sex' in request.GET:
	# 	sex = int(request.GET['sex'])
	# elif 'sex' in request.POST:
	# 	sex = int(request.POST['sex'])

	# if 'city' in request.GET:
	# 	city = request.GET['city']
	# elif 'city' in request.POST:
	# 	city = request.POST['city']

	current_user = User.objects.get(id=user_id)
	current_user.name = name
	current_user.sex = sex
	current_user.avatar = avatar
	current_user.city = city
	current_user.save()
	response['status'] = 0
	response['message'] = 'OK'	
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")	

###########################################
#
# 	账户相关
#
###########################################

@csrf_exempt
def create_channel(request):
	response = {}
	channel_id = None
	user_id = None
	title = ""
	cover = ""

	received_json_data = json.loads(request.body)
	channel_id = received_json_data['channel_id']
	user_id = received_json_data['user_id']
	if 'title' in received_json_data:
		title = received_json_data['title']
	if 'cover' in received_json_data:
		cover = received_json_data['cover']
	else:
		cover = current_user.avatar
	current_user = User.objects.get(id=user_id)
	current_channel = Channel.objects.get(channel_id=channel_id)

	current_channel.title = title
	current_channel.cover = cover
	current_channel.channel_status = 1 #开播
	current_channel.save()

	response['status'] = 0
	response['message'] = 'OK'	
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")		


# 关闭频道直播
@csrf_exempt
def close_channel(request):
	response = {}
	channel_id = None
	host_id = None	

	if 'channel_id' in request.POST:
		channel_id = int(request.POST['channel_id'])
	elif 'channel_id' in request.GET:
		channel_id = int(request.GET['channel_id'])

	if 'host_id' in request.POST:
		host_id = int(request.POST['host_id'])
	elif 'host_id' in request.GET:
		host_id = int(request.GET['host_id'])

	current_user = User.objects.get(id=host_id)
	current_channel = Channel.objects.get(channel_id=channel_id)

	current_channel.channel_status = 0 # 关闭直播
	current_channel.save()

	response['status'] = 0
	response['message'] = 'OK'	
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")		

# 获取下一次用户直播的频道号
@csrf_exempt
def get_next_broadcast_channel(request):
	response = {}

	user_id = None
	if 'user_id' in request.POST:
		user_id = int(request.POST['user_id'])
	elif 'user_id' in request.GET:
		user_id = int(request.GET['user_id'])

	current_user = User.objects.get(id=user_id)
	next_broadcast_channel = Channel.objects.get(user=current_user)
	response['status'] = 0
	response['message'] = 'OK'	
	response['data'] = {}
	response['data']['channel_id'] = next_broadcast_channel.channel_id
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")		


# 获取频道信息
def get_channel_info(request):
	response = {}
	channel_id = int(request.GET['channel_id'])
	current_channel = Channel.objects.get(channel_id=channel_id)
	response['status'] = 0
	response['message'] = 'OK'	
	response['data'] = {}	
	response['data']['channel_info'] = {}
	response['data']['channel_info']['audience_num'] = current_channel.audience_num
	response['data']['channel_info']['title'] = current_channel.title
	response['data']['channel_info']['cover'] = current_channel.cover
	response['data']['channel_info']['channel_id'] = current_channel.id
	response['data']['channel_info']['status'] = current_channel.channel_status
	# response['data']['channel_info']['create_time']
	response['data']['interact'] = []
	for interact_record in Interact.objects.filter(channel=current_channel):
		temp_interact_record = {}
		temp_interact_record['pos'] = interact_record.position
		temp_interact_record_user = interact_record.user
		temp_interact_record['user'] = {}
		temp_interact_record['user']['city'] = temp_interact_record_user.city
		temp_interact_record['user']['user_id'] = temp_interact_record_user.id
		temp_interact_record['user']['avatar'] = temp_interact_record_user.avatar
		temp_interact_record['user']['sex'] = temp_interact_record_user.sex
		temp_interact_record['user']['name'] = temp_interact_record_user.name
		temp_interact_record['user']['tim_id'] = TencentCloudUsreInfo.objects.get(user=temp_interact_record_user).tim_id

		response['data']['interact'].append(temp_interact_record)
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")		

# 获取房间当前直播人数
@csrf_exempt
def get_audience_num(request):
	response = {}	
	channel_id = None

	if 'channel_id' in request.POST:
		channel_id = int(request.POST['channel_id'])
	elif 'channel_id' in request.GET:
		channel_id = int(request.GET['channel_id'])	

	current_channel = Channel.objects.get(channel_id=channel_id)		
	current_channel.last_access_time = datetime.datetime.now()
	current_channel.save()

	response['status'] = 0
	response['message'] = 'OK'		
	response['data'] = {}
	response['data']['audience_num'] = current_channel.audience_num
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")		

# 获取直播列表
@csrf_exempt
def get_channel_list(request):
	response = {}	
	all_channels = Channel.objects.filter(channel_status=1)
	response['status'] = 0
	response['message'] = 'OK'		
	response['data'] = []
	for channel in all_channels:
		temp_channel_data = {}
		temp_channel_data['channel_info'] = {}
		temp_channel_data['host'] = {}
		channel_host = channel.user
		
		temp_channel_data['channel_info']['title'] = channel.title
		temp_channel_data['channel_info']['audience_num'] = channel.audience_num
		temp_channel_data['channel_info']['cover'] = channel.cover
		temp_channel_data['channel_info']['channel_id'] = channel.channel_id

		temp_channel_data['host']['city'] = channel_host.city
		temp_channel_data['host']['user_id'] = channel_host.id
		temp_channel_data['host']['avatar'] = channel_host.avatar
		temp_channel_data['host']['sex'] = channel_host.sex
		temp_channel_data['host']['name'] = channel_host.name
		temp_channel_data['host']['tim_id'] = TencentCloudUsreInfo.objects.get(user=channel_host).tim_id

		response['data'].append(temp_channel_data)
	# response['data']['audience_num'] = current_channel.audience_num
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")

# 添加喊麦
@csrf_exempt
def add_channel_interact(request):
	response = {}	
	channel_id = None
	user_id = None
	pos = None

	received_json_data = json.loads(request.body)
	channel_id = received_json_data['channel_id']
	user_id = received_json_data['user_id']
	pos = int(received_json_data['pos'])

	current_user = User.objects.get(id=user_id)
	current_channel = Channel.objects.get(channel_id=channel_id)

	for last_channel_interact in Interact.objects.filter(channel=current_channel,position=pos):
		last_channel_interact.delete()
	# 新增当前喊麦
	Interact.objects.create(channel=current_channel,user=current_user,position=pos)
	response['status'] = 0
	response['message'] = 'OK'	
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")

# 删除喊麦（离麦）
@csrf_exempt
def delete_channel_interact(request):
	response = {}	

	channel_id = None
	user_id = None
	pos = None

	received_json_data = json.loads(request.body)
	channel_id = received_json_data['channel_id']
	user_id = received_json_data['user_id']
	pos = int(received_json_data['pos'])

	current_user = User.objects.get(id=user_id)
	current_channel = Channel.objects.get(channel_id=channel_id)

	current_interact = Interact.objects.get(channel=current_channel,
		user=current_user,position=pos)
	current_interact.delete()

	response['status'] = 0
	response['message'] = 'OK'	
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")

# 用户进入直播间
@csrf_exempt
def add_channel_view_user(request):
	response = {}	

	channel_id = None
	user_id = None

	if 'channel_id' in request.POST:
		channel_id = int(request.POST['channel_id'])
	elif 'channel_id' in request.GET:
		channel_id = int(request.GET['channel_id'])
	
	if 'user_id' in request.POST:
		user_id = int(request.POST['user_id'])
	elif 'user_id' in request.GET:
		user_id = int(request.GET['user_id'])

	current_user = User.objects.get(id=user_id)
	current_channel = Channel.objects.get(channel_id=channel_id)

	current_user_view_record = UserChannelRecord.objects.create(channel=current_channel
		,user=current_user)
	current_channel.audience_num = current_channel.audience_num + 1
	current_channel.save()

	response['status'] = 0
	response['message'] = 'OK'	
	response['data'] = {}
	response['data']['channel_info'] = {}
	response['data']['channel_info']['audience_num'] = current_channel.audience_num

	response['data']['interact'] = []
	for interact_record in Interact.objects.filter(channel=current_channel):
		temp_interact_record = {}
		temp_interact_record['pos'] = interact_record.position
		temp_interact_record_user = interact_record.user
		temp_interact_record['user'] = {}
		temp_interact_record['user']['city'] = temp_interact_record_user.city
		temp_interact_record['user']['user_id'] = temp_interact_record_user.id
		temp_interact_record['user']['avatar'] = temp_interact_record_user.avatar
		temp_interact_record['user']['sex'] = temp_interact_record_user.sex
		temp_interact_record['user']['name'] = temp_interact_record_user.name
		temp_interact_record['user']['tim_id'] = TencentCloudUsreInfo.objects.get(user=temp_interact_record_user).tim_id

		response['data']['interact'].append(temp_interact_record)
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")


# 用户离开直播间
@csrf_exempt
def delete_channel_view_user(request):
	response = {}	

	channel_id = None
	user_id = None

	if 'channel_id' in request.POST:
		channel_id = int(request.POST['channel_id'])
	elif 'channel_id' in request.GET:
		channel_id = int(request.GET['channel_id'])
	
	if 'user_id' in request.POST:
		user_id = int(request.POST['user_id'])
	elif 'user_id' in request.GET:
		user_id = int(request.GET['user_id'])

	current_user = User.objects.get(id=user_id)
	current_channel = Channel.objects.get(channel_id=channel_id)

	for user_view_record in UserChannelRecord.objects.filter(channel=current_channel,user=current_user):
		user_view_record.delete()
		if current_channel.audience_num > 0:
			current_channel.audience_num = current_channel.audience_num - 1
	current_channel.save()

	response['status'] = 0
	response['message'] = 'OK'	
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")

# 获取直播间人员列表
@csrf_exempt
def channel_user_list(request):
	response = {}	

	channel_id = None

	if 'channel_id' in request.POST:
		channel_id = int(request.POST['channel_id'])
	elif 'channel_id' in request.GET:
		channel_id = int(request.GET['channel_id'])	

	current_channel = Channel.objects.get(channel_id=channel_id)

	response['status'] = 0
	response['message'] = 'OK'
	response['data'] = []
	for view_user in UserChannelRecord.objects.filter(channel=current_channel):
		temp_view_user_record = {}
		temp_view_user_record['city'] = view_user.user.city
		temp_view_user_record['user_id'] = view_user.user.id
		temp_view_user_record['avatar'] = view_user.user.avatar
		temp_view_user_record['sex'] = view_user.user.sex
		temp_view_user_record['name'] = view_user.user.name
		response['data'].append(temp_view_user_record)
	
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")


# 应用类

# 
@csrf_exempt
def minimize_start(request):
	response = {}
	received_json_data = json.loads(request.body)
	user_id = None
	if 'user_id' in received_json_data:
		user_id = int(received_json_data['user_id'])
	client_type = received_json_data['client_type']
	version = received_json_data['version']
	OS_version = received_json_data['OS_version']
	platform = received_json_data['platform']
	device_identifier = received_json_data['device_identifier']
	machine_type = received_json_data['machine_type']
	
	idfa = None
	if 'idfa' in received_json_data:
		idfa = received_json_data['idfa']
	
	device_token = None
	if 'device_token' in received_json_data:
		device_token = received_json_data['device_token']

	push_type = None
	if 'push_type' in received_json_data:
		push_type = int(received_json_data['push_type'])

	xiaomi_push = None
	if 'xiaomi_push' in received_json_data:
		xiaomi_push = received_json_data['xiaomi_push']

	huawei_push = None
	if 'huawei_push' in received_json_data:
		huawei_push = received_json_data['huawei_push']
	current_user = None
	if user_id:
		current_user = User.objects.get(id=user_id)

	response['status'] = 0
	response['message'] = 'OK'	

	if len(DeviceInfo.objects.filter(device_identifier=device_identifier)) == 0:
		if current_user:
			DeviceInfo.objects.create(user=current_user,client_type=client_type,version=version,
				os_version=OS_version,platform=platform,device_identifier=device_identifier,
				machine_type=machine_type,idfa=idfa,device_token=device_token,push_type=push_type,
				xiaomi_push=xiaomi_push,huawei_push=huawei_push)
		else:
			DeviceInfo.objects.create(client_type=client_type,version=version,
				os_version=OS_version,platform=platform,device_identifier=device_identifier,
				machine_type=machine_type,idfa=idfa,device_token=device_token,push_type=push_type,
				xiaomi_push=xiaomi_push,huawei_push=huawei_push)		

	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")

# device_token上报服务器
@csrf_exempt
def update_device_token(request):
	response = {}
	received_json_data = json.loads(request.body)

	user_id = int(received_json_data['user_id'])
	device_token = received_json_data['device_token']
	push_type = int(received_json_data['push_type'])

	current_user = User.objects.get(id=user_id)
	current_device_info = DeviceInfo.objects.get(user=current_user)
	current_device_info.device_token = device_token
	current_device_info.push_type = push_type
	current_device_info.save()

	response['status'] = 0
	response['message'] = 'OK'
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")

# 小米推送
@csrf_exempt
def xiaomi_message_push(request):
	response = {}
	received_json_data = json.loads(request.body)
	message = received_json_data['payload']
	package_name = received_json_data['restricted_package_name']
	pass_through = 0
	if 'pass_through' in received_json_data:
		pass_through = int(received_json_data['pass_through'])
	title = received_json_data['title']
	description = received_json_data['description']
	notify_type = -1
	if 'notify_type' in received_json_data:
		notify_type = int(received_json_data['notify_type'])
	key = WxPayConf_pub.XIAOMI_PUSH_APP_SECRET
	# import urllib2
	# 发起post请求
	params = {}
	headers = {"Authorization":"key=%s" % key}
	params['payload'] = message
	params['restricted_package_name'] = WxPayConf_pub.XIAOMI_PACKAGE_NAME
	params['pass_through'] = 0
	params['title'] = title
	params['description'] = description
	params['notify_type'] = notify_type

	response = requests.post("https://api.xmpush.xiaomi.com/v3/message/all",headers=headers,params=params)

	response['status'] = 0
	response['message'] = 'OK'	
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")	



# 友盟消息推送
@csrf_exempt
def upush_message(request):
	response = {}

	app_key = WxPayConf_pub.UPUSH_APP_KEY
	app_secret = WxPayConf_pub.UPUSH_MASTER_SECRET
	timestamp = str(time.time())[:10]
	url = 'http://msg.umeng.com/api/send'
	method = "POST"
	app_master_secret = WxPayConf_pub.UPUSH_MASTER_SECRET

	timestamp = int(time.time() * 1000 )
	method = 'POST'
	url = 'http://msg.umeng.com/api/send'
	params = {'appkey': app_key,
	          'timestamp': timestamp,
	          'type': 'broadcast',
	          'payload': {'body': {'ticker': 'Hello World',
	                               'title':'你好',
	                               'text':'来自友盟推送',
	                               'after_open': 'go_app'},
	                      'aps' : {'alert':'test'
	                      },
	                      'display_type': 'notification'
	          }
	}
	post_body = json.dumps(params)
	sign = md5('%s%s%s%s' % (method,url,post_body,app_master_secret))
	try:
	    r = urllib2.urlopen(url + '?sign='+sign, data=post_body)
	    print r.read()
	except urllib2.HTTPError,e:
	    print e.reason,e.read()
	except urllib2.URLError,e:
	    print e.reason
	response['status'] = 0
	response['message'] = 'OK'	
	print response
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")	

# 获取充值项目列表
def top_up_items(request):
	response = {}
	all_items = Item.objects.all()
	response['data'] = []
	for item in all_items:
		temp_item_data = {}
		if item.IAPId:
			temp_item_data['IAPId'] = item.IAPId
		temp_item_data['money'] = item.money
		temp_item_data['momentMoney'] = item.momentMoney
		if item.note:
			temp_item_data['note'] = item.note
			# temp_item_data['note'] = temp_item_data['note'].decode('utf-8')
		temp_item_data['itemId'] = item.id
		response['data'].append(temp_item_data)
	response['status'] = 0
	response['message'] = 'OK'	
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")		

# 苹果支付验证凭证
@csrf_exempt
def confirm_receipt(request):
	response = {}
	received_json_data = json.loads(request.body)
	user_id = int(received_json_data['user_id'])
	receipt_data = received_json_data['receiptData']
	itemId = int(received_json_data['itemId'])
	# IAPId = received_json_data['IAPId']
	# money = float(received_json_data['money'])
	momentMoney = float(received_json_data['momentMoney'])

	receipt_data_md5 = hashlib.md5(receipt_data).hexdigest()

	# 记录凭证记录
	AppleReceipt.objects.create(receipt_md5=receipt_data_md5)

	current_user = User.objects.get(id=user_id)
	current_item = Item.objects.get(id=itemId)

	# 记入购买item历史
	RechargeHistory.objects.create(user=current_user,item=current_item)

	# 更新账户金额
	current_account = Account.objects.get(user=current_user)
	current_account.amount += momentMoney
	current_account.save()

	response['status'] = 0
	response['message'] = 'OK'	
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")	

# 查看凭证是否有记录
@csrf_exempt
def check_receipt(request):
	response = {}
	received_json_data = json.loads(request.body)
	receipt_data = received_json_data['receiptData']
	receipt_data_md5 = hashlib.md5(receipt_data).hexdigest()
	if len(AppleReceipt.objects.filter(receipt_md5=receipt_data_md5)) == 0:
		response['status'] = 0
		response['message'] = 'OK'
	else:
		response['status'] = -1
		response['message'] = 'Receipt Data Exist!'
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")	

# 生成友盟签名
def generate_upush_sign(param_body,url,method,app_master_secret):
	sign = md5('%s%s%s%s' % (method,url,param_body,app_master_secret))
	return sign

# 客户端轮询
def round_check(request):
	response = {}
	all_actice_channels = Channel.objects.filter(channel_status=1)
	for activce_channel in all_actice_channels:
		seconds = (datetime.datetime.now() - activce_channel.last_access_time).total_seconds()
		if seconds > WxPayConf_pub.INACTIVE_SECONDS:
			activce_channel.channel_status = 0 
			activce_channel.save()
	response['status'] = 0
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")

def fetch_cos_sign(request):
	response = {}
	bucket = request.GET['bucket']
	bucket = bucket.encode('utf-8')
	appid = 10054072                  # 替换为用户的appid
	secret_id = u'AKIDgAHBtoaKNeazpseUJZbZ7auGbWFwA0Qt'.encode('utf-8')         # 替换为用户的secret_id
	secret_key = u'8qasXJ7vqkcTDz3aaUmJsdoMtobXMJXQ'.encode('utf-8')         # 替换为用户的secret_key
	
	now = int(time.time())
	expired = now + 300
	rdm = random.randint(0, 999999999)
	sign_tuple = (appid, secret_id, expired, now, rdm, bucket)

	plain_text = 'a=%s&k=%s&e=%d&t=%d&r=%d&b=%s&f=' % sign_tuple
	sha1_hmac   = hmac.new(secret_key, plain_text, hashlib.sha1)
	hmac_digest = sha1_hmac.hexdigest()
	hmac_digest = binascii.unhexlify(hmac_digest)
	sign_hex    = hmac_digest + plain_text
	sign_base64 = base64.b64encode(sign_hex)
	response['sign'] = repr(sign_base64)[1:-1]
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2),content_type="application/json")

def md5(s):
    m = hashlib.md5(s)
    return m.hexdigest()