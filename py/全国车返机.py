#!/usr/bin/env python3
"""
车牌号模糊手机号查询工具
基于ETCP API开发，用于查询车牌号对应的脱敏手机号信息
"""

import requests
import json
import time
from typing import Dict, List, Optional, Union


class CarNumberQuery:
    """车牌号查询工具类"""
    
    def __init__(self, user_id: str, token: str):
        """
        初始化查询工具
        
        Args:
            user_id: 用户ID
            token: 认证令牌
        """
        self.user_id = user_id
        self.token = token
        self.base_url = "https://ife.etcp.cn/api/v1/car/get-user-mobile-encrypt"
        
        # 请求头配置
        self.headers = {
            "Host": "ife.etcp.cn",
            "Connection": "keep-alive",
            "versionName": "5.5.0",
            "content-type": "application/x-www-form-urlencoded",
            "userId": str(user_id),
            "openId": "orbwc0aAfpQODfKs5go0Bqnt6FTk",
            "ayaya-v": "2.9.97",
            "ayaya-u": "176356879648763771",
            "version": "2.9.97",
            "token": token,
            "bizTime": self._get_current_timestamp(),
            "Accept-Encoding": "gzip,compress,br,deflate",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.60(0x18003c32) NetType/WIFI Language/zh_CN",
            "Referer": "https://servicewechat.com/wxc07f9d67923d676d/514/page-frame.html"
        }
    
    def _get_current_timestamp(self) -> str:
        """获取当前时间戳（毫秒）"""
        return str(int(time.time() * 1000))
    
    def _update_biz_time(self) -> None:
        """更新请求头中的时间戳"""
        self.headers["bizTime"] = self._get_current_timestamp()
    
    def query_car_number(self, car_number: str) -> Dict[str, Union[bool, str, Dict]]:
        """
        查询车牌号对应的模糊手机号
        
        Args:
            car_number: 车牌号
            
        Returns:
            查询结果字典
        """
        # 参数验证
        if not car_number or not car_number.strip():
            return {
                "success": False,
                "car_number": car_number,
                "error": "车牌号不能为空"
            }
        
        params = {
            "userId": self.user_id,
            "token": self.token,
            "carNumber": car_number.strip()
        }
        
        try:
            # 更新时间戳
            self._update_biz_time()
            
            # 发送请求
            response = requests.get(
                self.base_url, 
                params=params, 
                headers=self.headers, 
                timeout=10
            )
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            
            # 处理成功响应
            if result.get("code") == 0:
                data = result.get("data", {})
                return {
                    "success": True,
                    "car_number": car_number,
                    "encrypt_mobile": data.get("encryptMobilePhone", "未知"),
                    "bound_status": data.get("boundStatus", "未知"),
                    "is_owner": data.get("owner", False),
                    "raw_data": data
                }
            else:
                # 处理API返回的错误
                return {
                    "success": False,
                    "car_number": car_number,
                    "error_code": result.get("code"),
                    "message": result.get("message", "API请求失败"),
                    "raw_response": result
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "car_number": car_number,
                "error": "请求超时，请检查网络连接"
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "car_number": car_number,
                "error": "网络连接错误，请检查网络设置"
            }
        except requests.exceptions.HTTPError as e:
            return {
                "success": False,
                "car_number": car_number,
                "error": f"HTTP错误: {e.response.status_code}"
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "car_number": car_number,
                "error": f"网络请求异常: {str(e)}"
            }
        except json.JSONDecodeError:
            return {
                "success": False,
                "car_number": car_number,
                "error": "响应解析失败，返回格式不是有效的JSON"
            }
        except Exception as e:
            return {
                "success": False,
                "car_number": car_number,
                "error": f"未知错误: {str(e)}"
            }
    
    def batch_query(self, car_numbers: List[str]) -> List[Dict]:
        """
        批量查询多个车牌号
        
        Args:
            car_numbers: 车牌号列表
            
        Returns:
            查询结果列表
        """
        if not car_numbers:
            return []
        
        results = []
        total = len(car_numbers)
        
        for index, car_number in enumerate(car_numbers, 1):
            print(f"进度: {index}/{total} - 正在查询: {car_number}")
            
            result = self.query_car_number(car_number)
            results.append(result)
            
            # 添加延迟避免请求过快
            if index < total:  # 最后一个不需要延迟
                time.sleep(0.5)
        
        return results


class QueryInterface:
    """查询界面类"""
    
    def __init__(self, user_id: str, token: str):
        """初始化界面"""
        self.query_tool = CarNumberQuery(user_id, token)
    
    def display_result(self, result: Dict) -> None:
        """显示单条查询结果"""
        if result["success"]:
            print("✅ 查询成功!")
            print(f"   📍 车牌号: {result['car_number']}")
            print(f"   📱 模糊手机号: {result['encrypt_mobile']}")
            print(f"   🔗 绑定状态: {result['bound_status']}")
            print(f"   👤 是否车主: {'是' if result['is_owner'] else '否'}")
        else:
            print("❌ 查询失败!")
            error_msg = result.get('message') or result.get('error', '未知错误')
            print(f"   💥 错误信息: {error_msg}")
    
    def display_batch_results(self, results: List[Dict]) -> None:
        """显示批量查询结果"""
        print("\n" + "=" * 60)
        print("📊 批量查询结果汇总")
        print("=" * 60)
        
        success_count = 0
        for result in results:
            status = "✅" if result["success"] else "❌"
            if result["success"]:
                mobile = result.get("encrypt_mobile", "未知")
                success_count += 1
            else:
                mobile = result.get("message", result.get("error", "查询失败"))
            
            print(f"{status} {result['car_number']}: {mobile}")
        
        print("=" * 60)
        print(f"📈 统计: 成功 {success_count}/{len(results)}")
    
    def parse_car_numbers(self, input_text: str) -> List[str]:
        """解析输入的车牌号文本"""
        if not input_text.strip():
            return []
        
        # 支持多种分隔符
        separators = [',', '，', ' ', ';', '；', '、']
        input_text = input_text.strip()
        
        for sep in separators:
            if sep in input_text:
                return [num.strip() for num in input_text.split(sep) if num.strip()]
        
        # 如果没有分隔符，返回单个车牌号
        return [input_text]
    
    def single_query_mode(self) -> None:
        """单次查询模式"""
        print("\n🎯 单次查询模式")
        print("-" * 30)
        
        car_number = input("请输入车牌号: ").strip()
        if not car_number:
            print("⚠️  车牌号不能为空!")
            return
        
        print(f"\n🔍 正在查询车牌号: {car_number}...")
        result = self.query_tool.query_car_number(car_number)
        self.display_result(result)
    
    def batch_query_mode(self) -> None:
        """批量查询模式"""
        print("\n📋 批量查询模式")
        print("-" * 30)
        print("请输入多个车牌号，支持用逗号、空格等分隔:")
        
        input_text = input("车牌号: ").strip()
        if not input_text:
            print("⚠️  未输入车牌号!")
            return
        
        car_numbers = self.parse_car_numbers(input_text)
        if not car_numbers:
            print("⚠️  未找到有效的车牌号!")
            return
        
        print(f"\n🚀 开始批量查询 {len(car_numbers)} 个车牌号...")
        results = self.query_tool.batch_query(car_numbers)
        self.display_batch_results(results)
    
    def run(self) -> None:
        """运行主界面"""
        while True:
            print("\n" + "=" * 50)
            print("🚗 车牌号模糊手机号查询工具")
            print("=" * 50)
            print("请选择操作模式:")
            print("  1. 🎯 单次查询")
            print("  2. 📋 批量查询")
            print("  3. ❌ 退出程序")
            
            choice = input("\n请输入选择 (1/2/3): ").strip()
            
            if choice == "1":
                self.single_query_mode()
            elif choice == "2":
                self.batch_query_mode()
            elif choice == "3":
                print("\n👋 感谢使用，再见!")
                break
            else:
                print("⚠️  无效选择，请重新输入!")


def main():
    """主函数"""
    # 配置信息 - 请根据实际情况修改
    USER_ID = "208863719"
    TOKEN = "578a66a3-5f22-478d-bde7-f7afdb5c6978"
    
    try:
        # 创建查询界面并运行
        interface = QueryInterface(USER_ID, TOKEN)
        interface.run()
    except KeyboardInterrupt:
        print("\n\n👋 程序已被用户中断，再见!")
    except Exception as e:
        print(f"\n💥 程序发生异常: {str(e)}")
        print("请检查配置信息或网络连接后重试")


if __name__ == "__main__":
    main()