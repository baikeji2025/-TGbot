import requests
import json
import random

colors = [
    ''
]

print(random.choice(colors) + "白科技权威" + '')

url = "https://capi.tianyancha.com/cloud-tempest/app/searchCompany"
headers = {
    "Content-Type": "application/json",
    "xweb_xhr": "1",
    "Authorization": "0###oo34J0Y5dAD7qcjc1QWjyPjvsmIc###1700641997133###7ad8d272b9c4612d79492ee496f3b808",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309080f)XWEB/8461",
    "version": "TYC-XCX-WX",
    "Referer": "https://servicewechat.com/wx9f2867fc22873452/102/page-frame.html",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

search_term = input("请输入统一社会信用代码: ")
payload = {
    "sortType": 0,
    "pageSize": 20,
    "pageNum": 1,
    "word": search_term,
    "allowModifyQuery": 1
}
data = json.dumps(payload)

response = requests.post(url, headers=headers, data=data)
response_data = response.json()

if 'data' in response_data:
    company_data = response_data['data']['companyList'][0]

    company_name = company_data.get('name', '未知')
    legal_person = company_data.get('legalPersonName', '未知')
    establish_time = company_data.get('estiblishTime', '未知')
    reg_capital = company_data.get('regCapital', '未知')
    reg_location = company_data.get('regLocation', '未知')

    print(random.choice(colors) + f"公司名称: {company_name}" + '\033[0m')
    print(random.choice(colors) + f"法定代表人: {legal_person}" + '\033[0m')
    print(random.choice(colors) + f"注册时间: {establish_time}" + '\033[0m')
    print(random.choice(colors) + f"注册资金: {reg_capital}" + '\033[0m')
    print(random.choice(colors) + f"公司地址: {reg_location}" + '\033[0m')
    print(random.choice(colors) + '制作人:铭尘世.' + '\033[0m')
else:
    print("未找到相关数据")
