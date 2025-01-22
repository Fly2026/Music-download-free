import os
import json
import requests
from datetime import datetime, timedelta
import header

def verify(url):
    """验证登录并获取token"""
    try:
        # 发送验证码
        number = input("请输入你的手机号：")
        if len(number) != 11:
            print("手机号格式不对")
            return None
            
        # 发送验证码请求
        response = requests.get(f"{url}/captcha/sent?mobile={number}")
        response_data = response.json()
        
        if response_data.get("data") == '该号码发送的短信数已经超过上限':
            print(response_data["data"])
            return None
            
        # 输入验证码
        verify_number = input("验证码为：")
        response = requests.get(f"{url}/login/cellphone?mobile={number}&code={verify_number}")
        login_data = response.json()
        
        # 处理登录结果
        if login_data.get("data") == '该账号不存在':
            print("该账号不存在，可能手机号未注册")
            return None
        elif login_data.get("data") == '验证码错误':
            print("验证码错误，请重新输入")
            return verify(url)
            
        # 获取token和userid
        data = login_data
        userid = data.get('data', {}).get('userid')
        # 获取 token
        token = data.get('data', {}).get('token')
        
        if not token or not userid:
            print("登录失败：无法获取token或userid")
            return None
            
        # 生成token URL
        url_token = f"{url}/login/token?token={token}&userid={userid}"
        print(f"登录成功: {url_token}")
        
        # 获取cookies
        headers = header.head()
        response = requests.get(url_token, headers=headers)
        return response.cookies.get_dict()
        
    except Exception as e:
        print(f"登录过程中发生错误: {str(e)}")
        return None

def login(url):
    """登录并缓存cookies"""
    cache_file = "login_cache.json"
    headers = header.head()
    
    # 检查缓存文件是否存在且有效
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                
                # 检查缓存是否过期（1小时有效期）
                if datetime.now() < datetime.fromisoformat(cache['expire_time']):
                    return cache['cookies']
        except (json.JSONDecodeError, KeyError):
            pass  # 缓存无效，继续获取新token
    
    # 获取新token
    cookies = verify(url)
    if cookies:
        # 保存新缓存
        cache = {
            'cookies': cookies,
            'expire_time': (datetime.now() + timedelta(hours=1)).isoformat()
        }
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache, f)
        except Exception as e:
            print(f"保存登录缓存失败: {e}")
    
    return cookies
