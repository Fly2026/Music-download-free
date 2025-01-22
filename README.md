# Music-download-free
基于KugouMusic 概念版 API 获取音乐资源

# 音乐下载工具

这是一个基于Python的音乐下载工具，可以搜索、获取并下载音乐。

# API获取来源
通过
[MakcRe/KuGouMusicApi](https://github.com/MakcRe/KuGouMusicApi)
搭建的api平台
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
- `url.txt`: URL配置文件，这里放入上方api的网址头文件

## 使用方法

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 运行程序：
   ```bash
   python main.py
   ```

3.此时程序会跳转出一个window命令行窗口和一个GUI图形化界面

4.此前未登录过可以尝试先在GUI页面搜索任意文本，命令行窗口就会弹出酷狗音乐的登录界面，

  输入手机号和验证码即可获取用户token和id
- 目前仅支持手机号与验证码登录，一定要先去[酷狗官网](https://www.kugou.com/)注册手机号，否则会显示没有此账号

5.一切完成后，项目根目录会生成一个`login_cache.json`文件，该文件存储的是登录用户的缓存信息，有效期1小时，时间过后需要重新登录

6.在下载音乐时，根目录会生成`download`文件夹存储音乐文件

## 注意事项

在上方api平台搭建时，如果使用的屙屎由vercel所搭建的api平台，则由于其DNS污染，直接访问较慢，可以考虑自己添加一个域名（但是也会较慢，但是可以使用）

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
4. 有问题可以摘issues提出


