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
# Create your views here.

def get_user_sig(user_id):
	sig_user_id = WxPayConf_pub.USER_SIG_PREFIX + str(user_id)
	current_path = os.getcwd()
	sig_record_file_name = "sig_record_file_%s" % sig_user_id
	commands.getoutput("rm -rf %s" % sig_record_file_name)
	comds = current_path+"/tls_licence_tools gen ec_key.pem %s %d %s" % (sig_record_file_name,WxPayConf_pub.SDK_APPID,sig_user_id)
	commands.getoutput(current_path+"/tls_licence_tools gen ec_key.pem %s %d %s" % (sig_record_file_name,WxPayConf_pub.SDK_APPID,sig_user_id))
	result = commands.getoutput("cat %s" % sig_record_file_name )
	commands.getoutput("rm -rf %s" % sig_record_file_name)
	return result

def see_me(request):
	response = {}
	result = get_user_sig(5)
	print result
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

def a(request):
	response = {}
	api = TLSSigAPI(WxPayConf_pub.SDK_APPID, WxPayConf_pub.ECDSA_PRI_KEY)
	# # api = TLSSigAPI(WxPayConf_pub.SDK_APPID, WxPayConf_pub.ECDSA_PRI_KEY)
	sig = api.tls_gen_sig("xiaojun")
	# print sig
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

###########################################
#
# 	账户相关
#
###########################################

def third_party(request):
	response = {}
	auth_type = None
	third_party_id = None
	name = None
	sex = None
	avatar = None
	city = None

	if 'auth_type' in request.POST:
		auth_type = request.POST['auth_type']
	else:
		auth_type = request.GET['auth_type']

	if 'third_party_id' in request.POST:
		third_party_id = request.POST['third_party_id']
	else:
		third_party_id = request.GET['third_party_id']

	if 'name' in request.POST:
		name = request.POST['name']
	else:
		name = request.GET['name']

	if 'sex' in request.POST:
		sex = int(request.POST['sex'])
	else:
		sex = int(request.GET['sex'])

	if 'avatar' in request.POST:
		avatar = request.POST['avatar']
	else:
		avatar = request.GET['avatar']

	if 'city' in request.POST:
		city = request.POST['city']
	else:
		city = request.GET['city']

	users = User.objects.filter(third_party_id=third_party_id)
	new_user = None
	new_tim_id = None

	if len(users) > 0:
		new_user = users[0]
		new_tim_id = TencentCloudUsreInfo.objects.get(user=new_user)
	else:
		# 创建新用户
		new_user = User.objects.create(auth_type=auth_type,third_party_id=third_party_id,
			name=name,sex=sex,avatar=avatar,city=city)

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
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 刷新user_sig
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
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

###########################################
#
# 	礼物相关
#
###########################################

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
		temp_gift_record['icon_url'] = gift.icon_url
		temp_gift_record['name'] = gift.name
		response['data'].temp_gift_record

	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))


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
	gift_record = GiftRecord.objects.create(gift=current_gift,from_user=current_from_user,
		to_user=current_to_user,number=num)

	response['status'] = 0
	response['message'] = 'OK'
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

###########################################
#
# 	用户信息
#
###########################################

# 获取他人的个人信息
def other_profile(request):
	response = {}
	target_user_id = None
	if 'target_user_id' in request.GET:
		target_user_id = int(request.GET['target_user_id'])
	elif 'target_user_id' in request.POST:
		target_user_id = int(request.POST['target_user_id'])

	current_user = User.objects.get(id=target_user_id)

	received_gift_num = 0 # 收到礼物的数量
	recieved_gift_records = GiftRecord.objects.filter(to_user=current_user)
	for recieved_gift_record in recieved_gift_records:
		received_gift_num += recieved_gift_record.number

	sent_gift_num = 0 # 送出礼物的数量
	sent_gift_records = GiftRecord.objects.filter(from_user=current_user)
	for sent_gift_record in sent_gift_records:
		sent_gift_num += sent_gift_record.number

	response['status'] = 0
	response['message'] = 'OK'	
	response['data'] = {}
	response['data']['avatar'] = current_user.avatar
	response['data']['city'] = current_user.city
	response['data']['received_gift_num'] = received_gift_num
	response['data']['sent_gift_num'] = sent_gift_num
	response['data']['user_id'] = current_user.id
	response['data']['sex'] = current_user.sex
	response['data']['name'] = current_user.name
	response['data']['tim_id'] = TencentCloudUsreInfo.objects.get(user=current_user).tim_id
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))


def self_profile(request):
	response = {}
	user_id = None
	if 'user_id' in request.GET:
		user_id = int(request.GET['user_id'])
	elif 'user_id' in request.POST:
		user_id = int(request.POST['user_id'])

	current_user = User.objects.get(id=user_id)

	received_gift_num = 0 # 收到礼物的数量
	recieved_gift_records = GiftRecord.objects.filter(to_user=current_user)
	for recieved_gift_record in recieved_gift_records:
		received_gift_num += recieved_gift_record.number

	sent_gift_num = 0 # 送出礼物的数量
	sent_gift_records = GiftRecord.objects.filter(from_user=current_user)
	for sent_gift_record in sent_gift_records:
		sent_gift_num += sent_gift_record.number

	response['status'] = 0
	response['message'] = 'OK'	
	response['data'] = {}
	response['data']['user'] = {}
	response['data']['user']['avatar'] = current_user.avatar
	response['data']['user']['city'] = current_user.city
	response['data']['user']['received_gift_num'] = received_gift_num
	response['data']['user']['sent_gift_num'] = sent_gift_num
	response['data']['user']['user_id'] = current_user.id
	response['data']['user']['sex'] = current_user.sex
	response['data']['user']['name'] = current_user.name
	response['data']['user']['tim_id'] = TencentCloudUsreInfo.objects.get(user=current_user).tim_id
	response['data']['account'] = Account.objects.get(user=current_user).amount
	response['data']['account_verson'] = 10 # ?????
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))	

def user_update(request):
	response = {}
	user_id = None
	name = None
	avatar = None
	sex = None
	city = None
	if 'user_id' in request.GET:
		user_id = int(request.GET['user_id'])
	elif 'user_id' in request.POST:
		user_id = int(request.POST['user_id'])

	if 'name' in request.GET:
		name = request.GET['name']
	elif 'name' in request.POST:
		name = request.POST['name']

	if 'avatar' in request.GET:
		avatar = request.GET['avatar']
	elif 'avatar' in request.POST:
		avatar = request.POST['avatar']

	if 'sex' in request.GET:
		sex = int(request.GET['sex'])
	elif 'sex' in request.POST:
		sex = int(request.POST['sex'])

	if 'city' in request.GET:
		city = request.GET['city']
	elif 'city' in request.POST:
		city = request.POST['city']

	current_user = User.objects.get(id=user_id)
	current_user.name = name
	current_user.sex = sex
	current_user.avatar = avatar
	current_user.city = city
	current_user.save()
	response['status'] = 0
	response['message'] = 'OK'	
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))	

###########################################
#
# 	账户相关
#
###########################################

def create_channel(request):
	response = {}
	channel_id = None
	user_id = None
	title = ""
	cover = ""

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


	if 'title' in request.POST:
		title = request.POST['title']
	elif 'title' in request.GET:
		title = request.GET['title']
	# else:
	# 	title = current_user.avatar

	if 'cover' in request.POST:
		cover = request.POST['cover']
	elif 'cover' in request.GET:
		cover = request.GET['cover']
	else:
		cover = current_user.avatar

	current_channel.title = title
	current_channel.cover = cover
	current_channel.channel_status = 1 #开播
	current_channel.save()

	response['status'] = 0
	response['message'] = 'OK'	
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))		


# 关闭频道直播
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
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))		

# 获取下一次用户直播的频道号
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
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))		

# 获取房间当前直播人数
def get_audience_num(request):
	response = {}	
	channel_id = None

	if 'channel_id' in request.POST:
		channel_id = int(request.POST['channel_id'])
	elif 'channel_id' in request.GET:
		channel_id = int(request.GET['channel_id'])	

	current_channel = Channel.objects.get(channel_id=channel_id)		
	response['status'] = 0
	response['message'] = 'OK'		
	response['data'] = {}
	response['data']['audience_num'] = current_channel.audience_num
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))		

# 获取直播列表
def get_channel_list(request):
	response = {}	
	all_channels = Channel.objects.all()
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
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 添加喊麦
def add_channel_interact(request):
	response = {}	
	channel_id = None
	user_id = None
	pos = None

	if 'channel_id' in request.POST:
		channel_id = int(request.POST['channel_id'])
	elif 'channel_id' in request.GET:
		channel_id = int(request.GET['channel_id'])
	
	if 'user_id' in request.POST:
		user_id = int(request.POST['user_id'])
	elif 'user_id' in request.GET:
		user_id = int(request.GET['user_id'])

	if 'pos' in request.POST:
		pos = int(request.POST['pos'])
	elif 'pos' in request.GET:
		pos = int(request.GET['pos'])

	current_user = User.objects.get(id=user_id)
	current_channel = Channel.objects.get(channel_id=channel_id)

	for last_channel_interact in Interact.objects.filter(channel=current_channel,position=pos):
		last_channel_interact.delete()
	# 新增当前喊麦
	Interact.objects.create(channel=current_channel,user=current_user,position=pos)
	response['status'] = 0
	response['message'] = 'OK'	
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 删除喊麦（离麦）
def delete_channel_interact(request):
	response = {}	

	channel_id = None
	user_id = None
	pos = None

	if 'channel_id' in request.POST:
		channel_id = int(request.POST['channel_id'])
	elif 'channel_id' in request.GET:
		channel_id = int(request.GET['channel_id'])
	
	if 'user_id' in request.POST:
		user_id = int(request.POST['user_id'])
	elif 'user_id' in request.GET:
		user_id = int(request.GET['user_id'])

	if 'pos' in request.POST:
		pos = int(request.POST['pos'])
	elif 'pos' in request.GET:
		pos = int(request.GET['pos'])

	current_user = User.objects.get(id=user_id)
	current_channel = Channel.objects.get(channel_id=channel_id)

	current_interact = Interact.objects.get(channel=current_channel,
		user=current_user,position=pos)
	current_interact.delete()

	response['status'] = 0
	response['message'] = 'OK'	
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 用户进入直播间
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
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))


# 用户离开直播间
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
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))

# 获取直播间人员列表
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
		temp_view_user_record['city'] = view_user.city
		temp_view_user_record['user_id'] = view_user.id
		temp_view_user_record['avatar'] = view_user.avatar
		temp_view_user_record['sex'] = view_user.sex
		temp_view_user_record['name'] = view_user.name
		response['data'].append(temp_view_user_record)
	
	return HttpResponse(json.dumps(response,ensure_ascii=False,indent=2))
