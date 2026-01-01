import requests
import json
import time
import random
import hashlib
import hmac

class ChinaUnicomQuery:
    def __init__(self):
        self.base_url = "https://api.next.bspapp.com/client"
        self.space_id = "mp-8a2996fd-834e-4f76-8d17-4ea226dc161d"
        self.token = "e3c10ed1-a20c-4392-b42d-56a00c7f1846"
        
        # 生成随机设备ID
        self.device_id = self.generate_device_id()
        
    def generate_device_id(self):
        """生成随机设备ID"""
        timestamp = int(time.time() * 1000)
        random_num = random.randint(1000000000, 9999999999)
        return f"{timestamp}{random_num}"
    
    def generate_signature(self, params, timestamp):
        """生成签名"""
        secret_key = "your_secret_key_here"  # 需要根据实际情况获取
        message = f"{params}{timestamp}{secret_key}"
        return hmac.new(secret_key.encode(), message.encode(), hashlib.md5).hexdigest()
    
    def query_phone_balance(self, phone_number):
        """查询手机话费信息"""
        
        # 生成时间戳
        timestamp = int(time.time() * 1000)
        
        # 构建请求数据
        payload = {
            "method": "serverless.function.runtime.invoke",
            "params": json.dumps({
                "functionTarget": "xinhuafeiyuexhaxun",
                "functionArgs": {
                    "phonnumber": phone_number,
                    "isp": "中国联通",
                    "id": self.generate_device_id()[:24],  # 截取前24位作为ID
                    "ip": self.get_random_ip(),
                    "clientInfo": {
                        "PLATFORM": "mp-weixin",
                        "OS": "android",
                        "APPID": "__UNI__6F05BAF",
                        "DEVICEID": self.device_id,
                        "scene": 1037,
                        "appId": "__UNI__6F05BAF",
                        "appName": "tijan",
                        "appVersion": "1.0.0",
                        "appVersionCode": "100",
                        "appLanguage": "zh-Hans",
                        "hostVersion": "8.0.57",
                        "hostName": "SDK",
                        "uniPlatform": "mp-weixin",
                        "uniCompilerVersion": "4.75",
                        "uniRuntimeVersion": "4.75",
                        "deviceId": self.device_id,
                        "deviceType": "phone",
                        "deviceBrand": "redmi",
                        "deviceModel": "M2012K11AC",
                        "osName": "android",
                        "osVersion": "13",
                        "locale": "zh-Hans",
                        "LOCALE": "zh-Hans"
                    },
                    "uniIdToken": self.generate_token()
                }
            }),
            "spaceId": self.space_id,
            "timestamp": timestamp,
            "token": self.token
        }
        
        headers = {
            'Host': 'api.next.bspapp.com',
            'Connection': 'keep-alive',
            'Content-Length': str(len(json.dumps(payload))),
            'x-basement-token': self.token,
            'charset': 'utf-8',
            'x-serverless-sign': '6f112aab1eeee0980a597585c1663b53',  # 可能需要动态生成
            'User-Agent': 'Mozilla/5.0 (Linux; Android 13; M2012K11AC Build/TKQ1.221114.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.180 Mobile Safari/537.36 XWEB/1380275 MMWEBSDK/20240405 MMWEBID/2954 MicroMessenger/Lite Luggage/4.2.6 QQ/9.2.30.31725 NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android',
            'content-type': 'application/json',
            'Accept-Encoding': 'gzip,compress,br,deflate',
            'Referer': 'https://servicewechat.com/wx5f3dd72f16a42bf1/4/page-frame.html'
        }
        
        try:
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get('success'):
                data = result.get('data', {})
                return self.format_result(data)
            else:
                return f"查询失败: {result}"
                
        except requests.exceptions.RequestException as e:
            return f"请求错误: {str(e)}"
        except json.JSONDecodeError:
            return "响应解析错误"
    
    def get_random_ip(self):
        """生成随机IP地址"""
        return f"117.140.{random.randint(1, 255)}.{random.randint(1, 255)}"
    
    def generate_token(self):
        """生成模拟的uniIdToken"""
        # 这是一个简化的模拟，实际可能需要更复杂的JWT生成逻辑
        header = {"alg": "HS256", "typ": "JWT"}
        payload = {
            "uid": self.device_id[:24],
            "role": ["user"],
            "permission": [],
            "uniIdVersion": "1.0.16",
            "iat": int(time.time()),
            "exp": int(time.time()) + 2592000  # 30天过期
        }
        # 实际使用时需要正确的签名
        return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiI2OTIxYzE2MWI5ZmIyMzJiYTlkOWZiZGIiLCJyb2xlIjpbInVzZXIiXSwicGVybWlzc2lvbiI6W10sInVuaUlkVmVyc2lvbiI6IjEuMC4xNiIsImlhdCI6MTc2MzgxOTg3NywiZXhwIjoxNzY0MDc5MDc3fQ.BYjU_xnVdxZhM2iKtAR1mHXYvBHcDjmH05r-yJdah_0"
    
    def format_result(self, data):
        """格式化查询结果"""
        result = []
        result.append("=" * 40)
        result.append("联通手机话费查询结果")
        result.append("=" * 40)
        
        if data.get('userInfo'):
            result.append(f"用户姓名: {data['userInfo']}")
        result.append(f"手机号码: {data.get('phoneNumber', 'N/A')}")
        result.append(f"运营商: {data.get('isp_name', 'N/A')}")
        
        balance = data.get('balance', 0)
        if balance >= 0:
            result.append(f"当前余额: ¥{balance:.2f}")
        else:
            result.append(f"当前欠费: ¥{abs(balance):.2f}")
            
        result.append(f"用户类型: {data.get('type', 'N/A')}")
        result.append(f"套餐类型: {data.get('jikotype', 'N/A')}")
        
        create_time = data.get('createTime')
        if create_time:
            from datetime import datetime
            dt = datetime.fromtimestamp(create_time / 1000)
            result.append(f"查询时间: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
            
        result.append("=" * 40)
        return "\n".join(result)

def main():
    print("联通手机话费查询工具")
    print("查话费")
    print("-" * 40)
    
    query_tool = ChinaUnicomQuery()
    
    while True:
        phone_number = input("\n请输入联通手机号 (输入q退出): ").strip()
        
        if phone_number.lower() == 'q':
            print("感谢使用，再见！")
            break
            
        if not phone_number.isdigit() or len(phone_number) != 11:
            print("请输入有效的11位手机号码！")
            continue
            
        print(f"\n正在查询 {phone_number} 的话费信息...")
        result = query_tool.query_phone_balance(phone_number)
        print(result)

if __name__ == "__main__":
    main()