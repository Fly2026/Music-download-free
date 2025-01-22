# Music-download-free
基于KugouMusic 概念版 API 获取音乐资源

# 音乐下载工具

这是一个基于Python的音乐下载工具，可以搜索、获取并下载音乐。

## 功能特性

- 支持音乐搜索
- 获取音乐播放URL
- 下载音乐文件
- 用户登录功能
- 缓存登录信息

## 文件说明

- `main.py`: 主程序入口
- `api.py`: API接口封装
- `login.py`: 登录相关功能
- `search_music.py`: 音乐搜索功能
- `musicurl_get.py`: 获取音乐URL
- `download_music.py`: 音乐下载功能
- `header.py`: 请求头配置
- `url.txt`: URL配置文件

## 使用方法

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 运行程序：
   ```bash
   python main.py
   ```

## 依赖

- Python 3.x
- requests
- json
- os
- time

## 贡献指南

欢迎提交Pull Request！请确保：
1. 代码风格一致
2. 添加适当的注释
3. 更新相关文档

## 许可证

[MIT](LICENSE)

