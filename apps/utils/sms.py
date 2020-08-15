from ronglian_sms_sdk import SmsSDK
import random
import json

accId = '8aaf0708732220a60173d75664ce4f0f'
accToken = 'a7a49220c05b46b48a0dd42f25d42509'
appId = '8aaf0708732220a60173d75666024f16'


def send_message(phone):
    sdk = SmsSDK(accId, accToken, appId)
    tid = '1'
    mobile = phone
    code = str(random.randint(1000,9999))
    #缓存   设置键为 phone 值为code 过期时间180秒
    # cache.set(phone, code)
    # print(cache.get(phone))
    datas = (code, '1')
    resp = sdk.sendMessage(tid, mobile, datas)
    resp = json.loads(resp)
    return resp,code
