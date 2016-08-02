#coding:utf-8
'''
@author: dongshaohui
'''

class WxPayConf_pub(object):
	"""配置账号信息"""

	#=======【基本信息设置】=====================================
	# 腾讯云SDK APPID
	SDK_APPID = 1400012077
	ECDSA_PRI_KEY = """
-----BEGIN PRIVATE KEY-----
MIGEAgEAMBAGByqGSM49AgEGBSuBBAAKBG0wawIBAQQgPCYTfw+Q+3N1agaTKYnU
ApdVbXsTIs9Sgn7Rdqghx+OhRANCAARfepfnAwnPyCfpIeqttusbc2nMdWqXvH5Q
6Rx1U4EuVznT2nC22WHL4ZkdKOj6IsaUNdWvLfeRVSEKGNPoD0Cr
-----END PRIVATE KEY-----
"""
	USER_SIG_PREFIX = "maomen_test_" # 测试
	# USER_SIG_PREFIX = "maomen_product_" # 生产
	
	TIM_PREFIX = "maomen_test_" # 测试
	# TIM_PREFIX = "maomeo_product_" # 生产

	# 预留的频道数量
	RESERVED_CHANNEL_NUMBER = 1000 # 测试
	# RESERVED_CHANNEL_NUMBER = 3000 # 生产
	
	INACTIVE_SECONDS = 35 # 失效时间(秒)
	
	XIAOMI_PUSH_APP_SECRET = "X9tp+blGzOR7DVO73gfngg=="
	XIAOMI_PACKAGE_NAME = "com.zhelitech.moment"

	# umeng推送
	UPUSH_APP_KEY = "579f0ba067e58ed741000ab6"
	UPUSH_MASTER_SECRET = "qqbqnf4nqnk9trv1iybejj20xve4o6pf"
	
