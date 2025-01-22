import requests

def search(url, keyword, cookies):
    # 添加超时和重试机制
    session = requests.Session()
    retry_strategy = requests.adapters.HTTPAdapter(
        max_retries=3,
        pool_connections=10,
        pool_maxsize=100
    )
    session.mount("http://", retry_strategy)
    session.mount("https://", retry_strategy)
    
    try:
        response = session.get(
            f"{url}/search?keywords={keyword}",
            cookies=cookies,
            timeout=(3.05, 30)  # 连接超时3.05秒，读取超时30秒
        )
        response.raise_for_status()
        data = response.json()

        # 优化数据处理逻辑
        return [
            {
                "歌手": item['Singers'][0]['name'],
                "歌名": item['SongName'],
                "SQFileHash": item['SQFileHash']
            }
            for item in data['data']['lists']
            if item.get('SQFileHash')
        ]
    except requests.exceptions.RequestException as e:
        print(f"搜索请求失败: {e}")
        return []
    except (KeyError, IndexError) as e:
        print(f"数据解析失败: {e}")
        return []

