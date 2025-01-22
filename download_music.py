import os
import requests
from tqdm import tqdm
import musicurl_get

def on_download(song, artist, hash, url):
    """下载音乐文件"""
    try:
        # 获取下载链接
        download_url = musicurl_get.music_url(hash=hash, url=url)
        if not download_url:
            raise ValueError("无法获取下载链接")
            
        # 创建下载目录
        save_dir = "downloads"
        os.makedirs(save_dir, exist_ok=True)
        
        # 生成保存路径
        file_name = f"{song}-{artist}.mp3"
        save_path = os.path.join(save_dir, file_name)
        
        # 下载文件并显示进度
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 KB
        
        with open(save_path, 'wb') as file, tqdm(
            desc=file_name,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(block_size):
                size = file.write(data)
                bar.update(size)
                
        return save_path
        
    except requests.exceptions.RequestException as e:
        print(f"下载失败: {str(e)}")
        return None
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return None
