#coding=utf-8
from django.shortcuts import render
from broadcast.models import *
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.template.defaulttags import register
from django.db import transaction
from broadcast_conf import WxPayConf_pub
import OpenSSL
import base64
import zlib
import json
import time
import os,sys,commands
# Create your views here.


def list_all_curves():
    list = OpenSSL.crypto.get_elliptic_curves()
    for element in list:
        print element

def get_secp256k1():
    print OpenSSL.crypto.get_elliptic_curve('secp256k1');


def base64_encode_url(data):
    base64_data = base64.b64encode(data)
    base64_data = base64_data.replace('+', '*')
    base64_data = base64_data.replace('/', '-')
    base64_data = base64_data.replace('=', '_')
    return base64_data

def base64_decode_url(base64_data):
    base64_data = base64_data.replace('*', '+')
    base64_data = base64_data.replace('-', '/')
    base64_data = base64_data.replace('_', '=')
    raw_data = base64.b64decode(base64_data)
    return raw_data

class TLSSigAPI:
    """"""    
    __acctype = 0
    __identifier = ""
    __appid3rd = ""
    __sdkappid = 0
    __version = 20151204
    __expire = 3600*24*30       # 默认一个月，需要调整请自行修改
    __pri_key = ""
    __pub_key = ""
    _err_msg = "ok"

    def __get_pri_key(self):
        return OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, self.__pri_key);

    def __init__(self, sdkappid, pri_key):
        self.__sdkappid = sdkappid
        self.__pri_key = pri_key

    def __create_dict(self):
        m = {}
        m["TLS.account_type"] = "%d" % self.__acctype
        m["TLS.identifier"] = "%s" % self.__identifier
        m["TLS.appid_at_3rd"] = "%s" % self.__appid3rd
        m["TLS.sdk_appid"] = "%d" % self.__sdkappid
        m["TLS.expire_after"] = "%d" % self.__expire
        m["TLS.version"] = "%d" % self.__version
        m["TLS.time"] = "%d" % time.time()
        return m

    def __encode_to_fix_str(self, m):
        fix_str = "TLS.appid_at_3rd:"+m["TLS.appid_at_3rd"]+"\n" \
                  +"TLS.account_type:"+m["TLS.account_type"]+"\n" \
                  +"TLS.identifier:"+m["TLS.identifier"]+"\n" \
                  +"TLS.sdk_appid:"+m["TLS.sdk_appid"]+"\n" \
                  +"TLS.time:"+m["TLS.time"]+"\n" \
                  +"TLS.expire_after:"+m["TLS.expire_after"]+"\n"
        return fix_str

    def tls_gen_sig(self, identifier):
        self.__identifier = identifier

        m = self.__create_dict()
        fix_str = self.__encode_to_fix_str(m)
        pk_loaded = self.__get_pri_key()
        sig_field = OpenSSL.crypto.sign(pk_loaded, fix_str, "sha256");
        # sig_field_base64 = base64.b64encode(sig_field)
        # m["TLS.sig"] = sig_field_base64
        # json_str = json.dumps(m)
        # sig_cmpressed = zlib.compress(json_str)
        # base64_sig = base64_encode_url(sig_cmpressed)
        # return base64_sig 


def get_user_sig(user_id):
	sig_user_id = WxPayConf_pub.USER_SIG_PREFIX + str(user_id)
	current_path = os.getcwd()
	sig_record_file_name = "sig_record_file_%s" % sig_user_id
	commands.getoutput("rm -rf %s" % sig_record_file_name)
	comds = current_path+"/tls_licence_tools gen ec_key.pem %s %d %s" % (sig_record_file_name,WxPayConf_pub.SDK_APPID,sig_user_id)
	print comds
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