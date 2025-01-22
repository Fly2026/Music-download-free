import requests
import login
import json
from functools import lru_cache

# 添加缓存，最多缓存100个URL
@lru_cache(maxsize=100)
def music_url(hash, url):
    session = requests.Session()
    retry_strategy = requests.adapters.HTTPAdapter(
        max_retries=3,
        pool_connections=10,
        pool_maxsize=100
    )
    session.mount("http://", retry_strategy)
    session.mount("https://", retry_strategy)
    
    try:
        cookie = login.login(url)
        target_url = f"{url}/song/url?hash={hash}"
        response = session.get(
            target_url,
            cookies=cookie,
            timeout=(3.05, 30)  # 连接超时3.05秒，读取超时30秒
        )
        response.raise_for_status()
        data = response.json()
        
        # 更安全的URL提取
        urls = data.get("url", [])
        if urls and isinstance(urls, list):
            return urls[0]
        return None
    except requests.exceptions.RequestException as e:
        print(f"获取音乐URL失败: {e}")
        return None
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"数据解析失败: {e}")
        return None

