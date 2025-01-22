import tkinter as tk
from tkinter import ttk
import ctypes
import download_music,search_music,login

ctypes.windll.shcore.SetProcessDpiAwareness(2)


class MusicDownloadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("音乐下载软件")
        self.root.geometry("1000x800")

        # 顶部搜索区域
        self.search_frame = tk.Frame(self.root)
        self.search_frame.pack(pady=20)

        self.search_label = tk.Label(self.search_frame, text="音乐搜索：")
        self.search_label.pack(side=tk.LEFT, padx=5)

        self.search_entry = tk.Entry(self.search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        self.search_button = tk.Button(self.search_frame, text="搜索", command=self.on_search)
        self.search_button.pack(side=tk.LEFT, padx=5)

        # 结果表格区域
        self.tree_frame = tk.Frame(self.root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 设置表格样式
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview", 
                      rowheight=25,
                      font=('楷体', 10),
                      background="#FFFFFF",
                      fieldbackground="#FFFFFF",
                      bordercolor="#CCCCCC",
                      borderwidth=1,
                      relief="solid",
                      padding=0)
        
        style.configure("Treeview.Heading",
                      font=('楷体', 10, 'bold'),
                      background="#F0F0F0",
                      relief="flat")
        
        style.map("Treeview",
                 background=[("selected", "#0078D7")],
                 foreground=[("selected", "white")],
                 fieldbackground=[("selected", "#0078D7")])

        # 添加垂直滚动条
        self.scrollbar = ttk.Scrollbar(self.tree_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 创建表格
        self.tree = ttk.Treeview(self.tree_frame, 
                                columns=("song", "artist", "action"), 
                                show="headings",
                                selectmode="browse",
                                style="Treeview",
                                yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.config(command=self.tree.yview)

        # 设置表头
        self.tree.heading("song", text="歌名")
        self.tree.heading("artist", text="歌手")
        self.tree.heading("action", text="操作")

        # 设置列宽
        self.tree.column("song", width=300, anchor="center")
        self.tree.column("artist", width=200, anchor="center")
        self.tree.column("action", width=150, anchor="center")

        self.tree.pack(fill=tk.BOTH, expand=True)

    def on_search(self):
        """搜索按钮点击事件"""
        with open("url.txt","r") as f:
            url = f.read()
        search_text = self.search_entry.get().strip()
        
        if not search_text:
            return
            
        # 清空现有数据和按钮
        self.clear_results()
        
        # 显示加载状态
        self.tree.insert("", "end", values=("搜索中...", "", ""))
        self.root.update()
        
        try:
            cookies = login.login(url)
            all = search_music.search(search_text=search_text, url=url, cookies=cookies)
            
            if all == 1:
                cookies = login.login(url=url)
                all = search_music.search(search_text=search_text, url=url, cookies=cookies)
            
            if all and len(all) >= 4:
                music, hash_all, songs, songers = all
                
                # 清空加载状态
                self.clear_results()
                
                # 添加带下载按钮的结果
                music = all[0]
                hash_all = all[1]
                songs = all[2]
                songers = all[3]

                x = 0
                for i in music:
                    x += 1

                for i in range(x):  # 添加 5 行示例数据
                    urls = music[i]
                    self.tree.insert("", "end", values=(f"{urls[0]}", f"{urls[1]}", ""))
                    # 为每行创建按钮
                    button = ttk.Button(self.root, text=f"下载", 
                                command=lambda i=i: download_music.on_download(songs[i], songers[i], hash_all[i],url))  # 修正 button 的父组件
                    y_offset = 115 + i * 25  # 每行间隔 20 像素    # 计算按钮位置
                    button.place(relx=0.75, y=y_offset, height=24)
                    
        except Exception as e:
            self.clear_results()
            self.tree.insert("", "end", values=(f"搜索失败: {str(e)}", "", ""))
            
    def clear_results(self):
        """清空搜索结果"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
    def start_download(self, song, artist, hash, url):
        """启动下载任务"""
        # 在状态栏显示下载进度
        self.tree.insert("", "end", values=(f"正在下载: {song} - {artist}", "", ""))
        self.root.update()
        
        # 启动下载
        download_music.on_download(song, artist, hash, url)
        
        # 更新状态
        self.tree.insert("", "end", values=(f"下载完成: {song} - {artist}", "", ""))


if __name__ == "__main__":
    root = tk.Tk()
    app = MusicDownloadApp(root)
    root.mainloop()
