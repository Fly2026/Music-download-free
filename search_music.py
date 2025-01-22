import requests
import api

def search(search_text,url,cookies):
        result = api.search(url=url,keyword=search_text,cookies=cookies)
        # 处理 api 返回值
        music = []
        hash_all = []
        songers = []
        songs = []
        try:
            
            for x in result:
                songer = x["歌手"]
                songers.append(songer)
                song = x["歌名"]
                songs.append(song)  # 修正 songs 列表添加元素的错误
                hash_value = x["SQFileHash"]
                musicurl = (song, songer)
                music.append(musicurl)
                hash_all.append(hash_value)
            all = [music,hash_all,songs,songers]
            return all
        except:
            return 1
