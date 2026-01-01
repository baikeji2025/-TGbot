import requests
import json
import webbrowser
import os
import time
from datetime import datetime
import hashlib

class SmartImageManager:
    """智能图片管理器 - 确保总是获取最新图片"""
    
    def __init__(self):
        # 使用当前工作目录（编程软件根目录）
        self.current_dir = os.getcwd()
        print(f"📁 工作目录: {self.current_dir}")
    
    def get_latest_parking_image(self, plate_number):
        """获取最新的停车入场图片"""
        print(f"\n🔍 开始处理车牌 {plate_number}")
        
        # 1. 获取最新的订单信息
        latest_order = self.get_fresh_order_data(plate_number)
        if not latest_order:
            print("❌ 无法获取订单信息")
            return None
        
        # 显示完整订单详情
        self.display_full_order_details(latest_order)
        
        # 2. 提取订单关键信息用于比较
        current_order_info = self.extract_order_info(latest_order, plate_number)
        
        # 3. 检查是否有缓存图片
        cached_info = self.get_cached_order_info(plate_number)
        
        # 4. 判断是否需要更新图片
        need_update = self.need_image_update(current_order_info, cached_info)
        
        if need_update:
            print("🔄 检测到新图片，正在下载...")
            result = self.download_fresh_image(current_order_info)
        else:
            print("📁 使用现有的最新图片")
            cached_path = self.get_cached_image_path(plate_number)
            if cached_path and os.path.exists(cached_path):
                # 显示图片信息
                self.display_image_info(cached_path)
                webbrowser.open(cached_path)
                result = cached_path
            else:
                result = None
        
        return result
    
    def get_fresh_order_data(self, plate_number):
        """获取最新的订单数据"""
        url = "https://xbc.parking24.cn/payportal/getOrderInfo"
        headers = {
            "Host": "xbc.parking24.cn",
            "Connection": "keep-alive",
            "content-type": "application/json",
            "reformer-date": str(int(time.time() * 1000)),
            "reformer-user_id": "o5D7V5Jagvf5DTNeURSeD4L5r0zk",
            "reformer-sign": "xbc_wechat_mini:c9c1653860f332722a14909dc216236d",
            "Accept-Encoding": "gzip,compress,br,deflate",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.60(0x18003c32) NetType/WIFI Language/zh_CN",
            "Referer": "https://servicewechat.com/wx794c445a464f7d5d/180/page-frame.html"
        }
        
        data = {
            "serial_no": "",
            "type": "",
            "car_park_id": "",
            "user_id": "o5D7V5Jagvf5DTNeURSeD4L5r0zk",
            "plate_no": plate_number,
            "plate_no_color": "0000FF00",
            "charge_terminal": "2100",
            "charge_channel": "3000",
            "billing_id": plate_number,
            "billing_type": "1",
            "business_type": 1,
            "service_no": "1",
            "order_no": "",
            "discount_codes": [],
            "goods_data": [],
            "acs_good_list": [],
            "expand": {
                "type": "",
                "qrcode_series_no": "",
                "lane_id": "",
                "lane_type": "",
                "box_datetime": "",
                "xb_uid": "fedba1abb2624854bc0e7d5908e80d9e",
                "aliCertId": "",
                "aliPromoParam": "",
                "aliPromoAmount": ""
            },
            "requestTaskKey": "request_key_getOrderInfo",
            "taskKey": "GetOrderInfo_default"
        }
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            result = response.json()
            
            if result.get('code') == '200':
                print("✅ 获取到最新订单数据")
                return result
            else:
                print(f"❌ 订单查询失败: {result.get('msg')}")
                return None
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return None
    
    def display_full_order_details(self, order_data):
        """显示完整的订单详情"""
        if not order_data or 'data' not in order_data:
            print("❌ 无订单数据可显示")
            return
            
        data = order_data['data']
        expand_data = data.get('expand_data', {})
        
        print("\n" + "="*60)
        print("📋 完整订单信息")
        print("="*60)
        
        # 基本车辆信息
        print(f"🚗 车牌号码: {data.get('plate_no', 'N/A')}")
        print(f"🏢 停车场: {data.get('provider_name', 'N/A')}")
        print(f"🆔 停车场ID: {data.get('car_park_id', 'N/A')}")
        
        # 时间信息
        print(f"🕒 入场时间: {expand_data.get('entering_datetime', 'N/A')}")
        
        # 计算停车时长（从毫秒转换为可读格式）
        parking_duration_ms = expand_data.get('parking_duration', 0)
        if parking_duration_ms:
            total_seconds = parking_duration_ms // 1000
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            print(f"⏱️ 停车时长: {hours}小时{minutes}分钟{seconds}秒")
        
        # 费用信息
        print(f"💰 应付金额: {data.get('amount_receivable', 'N/A')} 元")
        print(f"💳 实付金额: {data.get('amount_actual', 'N/A')} 元")
        print(f"💵 已付金额: {data.get('amount_received', 'N/A')} 元")
        print(f"🎫 优惠金额: {data.get('discount_amount', 'N/A')} 元")
        
        # 订单信息
        print(f"📄 订单号: {data.get('order_no', 'N/A')}")
        print(f"📊 订单状态: {data.get('order_status', 'N/A')}")
        print(f"🔄 业务类型: {data.get('business_type_name', 'N/A')}")
        
        # 支付信息
        payment_time = data.get('payment_datetime', 0)
        if payment_time and payment_time > 0:
            # 将时间戳转换为可读格式
            payment_date = datetime.fromtimestamp(payment_time/1000).strftime('%Y-%m-%d %H:%M:%S')
            print(f"💳 支付时间: {payment_date}")
        else:
            print("💳 支付状态: 未支付")
        
        print("="*60)
    
    def extract_order_info(self, order_data, plate_number):
        """从订单数据中提取关键信息"""
        data = order_data.get('data', {})
        expand_data = data.get('expand_data', {})
        
        # 提取图片URL
        image_url = expand_data.get('entering_image')
        if not image_url:
            image_url = data.get('extand', {}).get('entering_image')
        
        # 提取入场时间
        entering_time = expand_data.get('entering_datetime')
        
        # 提取订单号
        order_no = data.get('order_no')
        
        # 计算信息哈希（用于判断是否发生变化）
        info_string = f"{image_url}|{entering_time}|{order_no}"
        info_hash = hashlib.md5(info_string.encode()).hexdigest()
        
        return {
            'plate_number': plate_number,
            'image_url': image_url,
            'entering_time': entering_time,
            'order_no': order_no,
            'info_hash': info_hash,
            'timestamp': time.time()
        }
    
    def get_cached_order_info(self, plate_number):
        """获取缓存的订单信息"""
        cache_file = os.path.join(self.current_dir, f"{plate_number}_info.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return None
    
    def save_order_info(self, order_info):
        """保存订单信息到缓存"""
        cache_file = os.path.join(self.current_dir, f"{order_info['plate_number']}_info.json")
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(order_info, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存缓存信息失败: {e}")
    
    def need_image_update(self, current_info, cached_info):
        """判断是否需要更新图片"""
        if not cached_info:
            print("📝 无缓存记录，需要下载新图片")
            return True
        
        # 比较信息哈希值
        if current_info['info_hash'] != cached_info.get('info_hash'):
            print("🆕 检测到订单信息变化，需要更新图片")
            return True
        
        # 检查图片文件是否存在
        cached_image_path = self.get_cached_image_path(current_info['plate_number'])
        if not os.path.exists(cached_image_path):
            print("📝 缓存图片不存在，需要重新下载")
            return True
        
        # 检查缓存图片是否过期（超过30分钟）
        cache_age = time.time() - cached_info.get('timestamp', 0)
        if cache_age > 1800:  # 30分钟
            print("🕒 缓存图片已过期，需要重新下载")
            return True
        
        print("✅ 缓存图片仍然有效")
        return False
    
    def download_fresh_image(self, order_info):
        """下载最新的图片"""
        if not order_info.get('image_url'):
            print("❌ 没有可用的图片URL")
            return None
        
        image_url = order_info['image_url']
        plate_number = order_info['plate_number']
        
        print(f"📷 下载图片: {image_url}")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_4_1 like Mac OS X) AppleWebKit/605.1.15'
            }
            response = requests.get(image_url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                # 生成文件名 - 直接保存在当前目录
                timestamp = int(time.time())
                filename = f"{plate_number}_入场图片_{timestamp}.jpg"
                file_path = os.path.join(self.current_dir, filename)
                
                # 保存图片
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                
                # 更新缓存信息
                order_info['image_file'] = filename
                self.save_order_info(order_info)
                
                # 删除旧的缓存图片（如果有）
                self.cleanup_old_images(plate_number, filename)
                
                print(f"✅ 最新图片已保存: {file_path}")
                
                # 显示图片信息
                self.display_image_info(file_path)
                
                # 在浏览器中打开
                webbrowser.open(file_path)
                return file_path
            else:
                print(f"❌ 下载失败，HTTP状态码: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ 下载图片时出错: {e}")
            return None
    
    def display_image_info(self, image_path):
        """显示图片信息"""
        if os.path.exists(image_path):
            file_size = os.path.getsize(image_path)
            file_size_kb = file_size / 1024
            file_time = datetime.fromtimestamp(os.path.getmtime(image_path)).strftime('%Y-%m-%d %H:%M:%S')
            
            print("\n" + "-"*40)
            print("🖼️ 图片信息")
            print("-"*40)
            print(f"📁 文件路径: {image_path}")
            print(f"📏 文件大小: {file_size_kb:.2f} KB")
            print(f"🕐 下载时间: {file_time}")
            print(f"🔗 图片类型: JPEG")
            print("-"*40)
    
    def get_cached_image_path(self, plate_number):
        """获取缓存图片路径"""
        info_file = os.path.join(self.current_dir, f"{plate_number}_info.json")
        if os.path.exists(info_file):
            try:
                with open(info_file, 'r', encoding='utf-8') as f:
                    info = json.load(f)
                    image_file = info.get('image_file')
                    if image_file:
                        return os.path.join(self.current_dir, image_file)
            except:
                pass
        return None
    
    def cleanup_old_images(self, plate_number, keep_filename):
        """清理旧的缓存图片"""
        try:
            for filename in os.listdir(self.current_dir):
                if filename.startswith(f"{plate_number}_入场图片_") and filename.endswith(".jpg") and filename != keep_filename:
                    old_path = os.path.join(self.current_dir, filename)
                    if os.path.isfile(old_path):
                        os.remove(old_path)
                        print(f"🗑️ 已删除旧图片: {filename}")
        except Exception as e:
            print(f"清理旧图片时出错: {e}")

def main_smart_system():
    """智能图片管理系统主函数"""
    print("=" * 70)
    print("🤖 智能停车场图片管理系统")
    print("=" * 70)
    print("特点:")
    print("- 🔄 自动检测是否有新图片")
    print("- 💾 智能缓存管理")
    print("- 🆕 总是优先使用最新图片")
    print("- 🗑️ 自动清理旧图片")
    print("- 📊 显示完整订单信息")
    print("- 🖼️ 显示图片详细信息")
    print("- 📁 图片保存在当前工作目录")
    print("=" * 70)
    
    image_manager = SmartImageManager()
    
    while True:
        print("\n" + "-" * 50)
        plate_input = input("请输入车牌号 (输入 'q' 退出): ").strip()
        
        if plate_input.lower() in ['q', 'quit', 'exit']:
            print("感谢使用，再见！👋")
            break
        
        if not plate_input:
            continue
        
        # 格式化车牌号
        plate_number = plate_input.upper().replace(' ', '').replace('·', '')
        
        # 获取最新图片
        result = image_manager.get_latest_parking_image(plate_number)
        
        if result:
            print(f"\n🎉 处理完成！")
            print(f"📁 图片已保存到项目根目录: {os.path.basename(result)}")
        else:
            print(f"\n❌ 无法获取车牌 {plate_number} 的图片")

if __name__ == "__main__":
    main_smart_system()