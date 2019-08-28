from celery_tasks.main import app
from .yuntongxun.sms import CCP
from . import constant

@app.task(name="send_sms")
def send_sms(mobile, sms_code):
    ccp = CCP()
    result = ccp.send_template_sms(mobile, [sms_code, constant.SMS_EXPIRE_TIME // 60], constant.SMS_TEIMPLATE_ID)
    if result == -1:
        return "发送短信失败"
    else:
        return "发送短信成功"