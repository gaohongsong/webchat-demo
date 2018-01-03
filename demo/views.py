# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import hashlib
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException
from wechatpy import parse_message, create_reply
from wechatpy.crypto import WeChatCrypto


app_id = ''
token = ''
encoding_aes_key = ''

#django默认开启csrf防护，这里使用@csrf_exempt去掉防护
@csrf_exempt
def echo(request):
    if request.method == "GET":
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
	
	try:
	    check_signature(token, signature, timestamp, nonce)
	except InvalidSignatureException:
            return HttpResponse('failed')

        return HttpResponse(echostr)

    else:
        signature = request.GET.get('signature', None)
        msg_signature = request.GET.get('msg_signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        encrypt_type = request.GET.get('encrypt_type', None)
	xml = request.body

	#print signature, timestamp, nonce, encrypt_type, msg_signature

	crypto = WeChatCrypto(token, encoding_aes_key, app_id)
	try:
	    # print 'encryped xml: %s' % xml
    	    decrypted_xml = crypto.decrypt_message(
        	xml,
        	msg_signature,
        	timestamp,
        	nonce
    	    )
	    # print 'decryped xml: %s' % decrypted_xml
	except (InvalidAppIdException, InvalidSignatureException):
    	    # 处理异常或忽略
    	    pass

	msg = parse_message(decrypted_xml)

        if msg.type == 'text':
	    print 'message arrived[%s]: %s' % (msg.type, msg.content)
            reply = create_reply(msg.content, msg)
        else:
	    print 'message arrived[%s]: %s' % (msg.type, 'not support')
            reply = create_reply('Sorry, can not handle this for now', msg)
	
        encrypted_msg = crypto.encrypt_message(
            reply.render(),
            nonce,
            timestamp
        )
	return HttpResponse(encrypted_msg)
