#https://t.me/QWSJSTFX删除死马
#https://t.me/QWSJSTFX删除死马
#https://t.me/QWSJSTFX删除死马
#https://t.me/QWSJSTFX删除死马
#https://t.me/QWSJSTFX删除死马
#https://t.me/QWSJSTFX删除死马
#https://t.me/QWSJSTFX删除死马
#https://t.me/QWSJSTFX删除死马
#https://t.me/QWSJSTFX删除死马
#https://t.me/QWSJSTFX删除死马
#https://t.me/QWSJSTFX删除死马
#https://t.me/QWSJSTFX删除死马
#https://t.me/QWSJSTFX删除死马
#https://t.me/QWSJSTFX删除死马
import requests

def sensitive_library_query():
    # 获取用户输入，明确提示身份证号格式
    id_card = input("请输入要查询的身份证号（例：110101199001011234）：").strip()
    
    # 前置校验：空输入拦截+身份证号格式简单验证（18位）
    if not id_card:
        print("错误：身份证号不能为空，请重新输入！")
        return
    if not (len(id_card) == 18 and (id_card[:17].isdigit() and id_card[-1].isdigit() or id_card[-1].upper() == 'X')):
        print("错误：请输入18位有效身份证号（最后一位可为X）！")
        return
    
    # 拼接API地址，确保msg参数正确传递身份证号
    api_url = f"http://api.kona.uno/API/mgk.php?msg={id_card}"
    
    try:
        # 发送GET请求，设置10秒超时防止卡顿
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()  # 状态码非200时抛出异常
        
        # 直接返回API原始结果
        print("\nAPI查询结果：")
        print(response.text)
        
    except requests.exceptions.Timeout:
        print("\n错误：网络超时，请检查网络连接后重试！")
    except requests.exceptions.RequestException as e:
        print(f"\n请求失败：{str(e)}")
    except Exception as e:
        print(f"\n未知错误：{str(e)}")

# 执行查询
if __name__ == "__main__":
    sensitive_library_query()
