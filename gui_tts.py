#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文字转语音GUI程序
提供图形界面进行文字转语音操作
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from tts import TTSEngine
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保已安装所需依赖: pip install -r requirements.txt")
    sys.exit(1)


class TTSGui:
    """文字转语音GUI应用程序"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("文字转语音程序")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # 初始化TTS引擎
        self.tts_engine = None
        self.is_playing = False
        
        # 创建界面
        self.create_widgets()
        
        # 初始化TTS引擎
        self.init_tts_engine()
    
    def create_widgets(self):
        """创建GUI组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="文字转语音程序", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 文本输入区域
        text_label = ttk.Label(main_frame, text="请输入要转换的文本：")
        text_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
        
        self.text_area = scrolledtext.ScrolledText(
            main_frame, 
            width=60, 
            height=10,
            wrap=tk.WORD,
            font=("Arial", 12)
        )
        self.text_area.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=(0, 20))
        
        # 设置区域
        settings_frame = ttk.LabelFrame(main_frame, text="设置", padding="10")
        settings_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(0, 20))
        settings_frame.columnconfigure(1, weight=1)
        settings_frame.columnconfigure(3, weight=1)
        
        # 语速设置
        ttk.Label(settings_frame, text="语速:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.rate_var = tk.IntVar(value=200)
        self.rate_scale = ttk.Scale(
            settings_frame, 
            from_=50, 
            to=400, 
            variable=self.rate_var,
            orient=tk.HORIZONTAL,
            length=150
        )
        self.rate_scale.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        self.rate_label = ttk.Label(settings_frame, text="200")
        self.rate_label.grid(row=0, column=2, padx=(0, 20))
        
        # 音量设置
        ttk.Label(settings_frame, text="音量:").grid(row=0, column=3, sticky=tk.W, padx=(0, 5))
        self.volume_var = tk.DoubleVar(value=0.9)
        self.volume_scale = ttk.Scale(
            settings_frame, 
            from_=0.0, 
            to=1.0, 
            variable=self.volume_var,
            orient=tk.HORIZONTAL,
            length=150
        )
        self.volume_scale.grid(row=0, column=4, sticky="ew", padx=(0, 10))
        self.volume_label = ttk.Label(settings_frame, text="0.9")
        self.volume_label.grid(row=0, column=5)
        
        # 引擎选择
        ttk.Label(settings_frame, text="引擎:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0), padx=(0, 5))
        self.engine_var = tk.StringVar(value="auto")
        engine_frame = ttk.Frame(settings_frame)
        engine_frame.grid(row=1, column=1, columnspan=5, sticky=tk.W, pady=(10, 0))
        
        ttk.Radiobutton(engine_frame, text="自动选择", variable=self.engine_var, value="auto").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(engine_frame, text="离线引擎", variable=self.engine_var, value="offline").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(engine_frame, text="在线引擎", variable=self.engine_var, value="online").pack(side=tk.LEFT)
        
        # 绑定滑块事件
        self.rate_scale.configure(command=self.update_rate_label)
        self.volume_scale.configure(command=self.update_volume_label)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(0, 10))
        
        self.play_button = ttk.Button(
            button_frame, 
            text="播放语音", 
            command=self.play_speech,
            style="Accent.TButton"
        )
        self.play_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(
            button_frame, 
            text="停止播放", 
            command=self.stop_speech,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame, 
            text="清空文本", 
            command=self.clear_text
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame, 
            text="示例文本", 
            command=self.load_example
        ).pack(side=tk.LEFT)
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(10, 0))
        
        # 快捷键绑定
        self.root.bind('<Control-Return>', lambda e: self.play_speech())
        self.root.bind('<Escape>', lambda e: self.stop_speech())
        self.text_area.focus()
    
    def update_rate_label(self, value):
        """更新语速标签"""
        self.rate_label.config(text=str(int(float(value))))
    
    def update_volume_label(self, value):
        """更新音量标签"""
        self.volume_label.config(text=f"{float(value):.1f}")
    
    def init_tts_engine(self):
        """初始化TTS引擎"""
        try:
            self.tts_engine = TTSEngine()
            self.status_var.set("TTS引擎初始化成功")
        except Exception as e:
            self.status_var.set(f"TTS引擎初始化失败: {e}")
            messagebox.showerror("错误", f"TTS引擎初始化失败:\n{e}\n\n程序将继续运行，但语音功能可能不可用。")
            self.tts_engine = None  # 确保设置为None以便后续检查
    
    def play_speech(self):
        """播放语音"""
        try:
            if self.is_playing:
                messagebox.showwarning("警告", "正在播放中，请等待完成或停止当前播放")
                return
            
            text = self.text_area.get("1.0", tk.END).strip()
            if not text:
                messagebox.showwarning("警告", "请输入要转换的文本")
                return
            
            if not self.tts_engine:
                messagebox.showerror("错误", "TTS引擎未初始化，请重启程序")
                return
            
            # 更新引擎设置
            try:
                self.tts_engine.set_rate(self.rate_var.get())
                self.tts_engine.set_volume(self.volume_var.get())
            except Exception as e:
                print(f"设置引擎参数时发生错误: {e}")
                # 继续执行，不中断播放流程
            
            # 在新线程中播放语音
            self.is_playing = True
            self.play_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_var.set("正在播放语音...")
        
        except Exception as e:
            print(f"播放语音时发生错误: {e}")
            messagebox.showwarning("警告", f"播放语音时发生错误:\n{e}\n\n程序将继续运行。")
            self.reset_play_state()
            return
        
        def play_thread():
            try:
                engine_mode = self.engine_var.get()
                force_online = (engine_mode == "online")
                
                if engine_mode == "offline" and (not self.tts_engine or not self.tts_engine.offline_engine):
                    self.root.after(0, lambda: messagebox.showerror("错误", "离线引擎不可用，请选择其他引擎"))
                    return
                
                if self.tts_engine:
                    success = self.tts_engine.speak(text, force_online=force_online)
                else:
                    success = False
                
                if success:
                    self.root.after(0, lambda: self.status_var.set("播放完成"))
                else:
                    self.root.after(0, lambda: self.status_var.set("播放失败"))
                    self.root.after(0, lambda: messagebox.showwarning("警告", "语音播放失败，请检查网络连接或尝试其他引擎"))
                    
            except Exception as e:
                error_msg = str(e)
                self.root.after(0, lambda: self.status_var.set(f"播放错误: {error_msg}"))
                self.root.after(0, lambda: messagebox.showwarning("警告", f"播放过程中发生错误:\n{error_msg}\n\n程序将继续运行。"))
            finally:
                self.root.after(0, self.reset_play_state)
        
        threading.Thread(target=play_thread, daemon=True).start()
    
    def stop_speech(self):
        """停止播放"""
        try:
            # 调用TTS引擎的停止方法
            if self.tts_engine:
                self.tts_engine.stop()
            
            # 重置UI状态
            self.reset_play_state()
            self.status_var.set("播放已停止")
        except Exception as e:
            print(f"停止播放时发生错误: {e}")
            # 确保UI状态被重置
            try:
                self.reset_play_state()
            except:
                pass
    
    def reset_play_state(self):
        """重置播放状态"""
        try:
            self.is_playing = False
            self.play_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
        except Exception as e:
            print(f"重置播放状态时发生错误: {e}")
            # 强制重置播放状态
            self.is_playing = False
    
    def clear_text(self):
        """清空文本"""
        try:
            self.text_area.delete("1.0", tk.END)
            self.text_area.focus()
            self.status_var.set("文本已清空")
        except Exception as e:
            print(f"清空文本时发生错误: {e}")
            messagebox.showwarning("警告", "清空文本时发生错误，但程序将继续运行")
    
    def load_example(self):
        """加载示例文本"""
        try:
            examples = [
                "你好，欢迎使用文字转语音程序！",
                "Hello, welcome to the text-to-speech program!",
                "这是一个支持中英文的语音合成系统。",
                "This system supports both Chinese and English text-to-speech conversion.",
                "人工智能技术正在改变我们的生活方式。",
                "Artificial intelligence is transforming the way we live."
            ]
            
            import random
            example = random.choice(examples)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", example)
            self.status_var.set("已加载示例文本")
        except Exception as e:
            print(f"加载示例文本时发生错误: {e}")
            messagebox.showwarning("警告", "加载示例文本时发生错误，但程序将继续运行")


def main():
    """主函数"""
    try:
        # 创建主窗口
        root = tk.Tk()
        
        # 设置窗口图标（如果有的话）
        try:
            # 可以在这里设置窗口图标
            # root.iconbitmap('icon.ico')
            pass
        except:
            pass
        
        # 创建应用程序
        app = TTSGui(root)
        
        # 设置窗口关闭事件
        def on_closing():
            try:
                if app.is_playing:
                    if messagebox.askokcancel("退出", "正在播放语音，确定要退出吗？"):
                        root.destroy()
                else:
                    root.destroy()
            except Exception as e:
                print(f"关闭窗口时发生错误: {e}")
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # 在状态栏显示使用提示，而不是弹出对话框
        try:
            app.status_var.set("就绪 - 快捷键: Ctrl+Enter播放, Esc停止")
        except Exception as e:
            print(f"设置状态信息时发生错误: {e}")
        
        # 启动GUI
        root.mainloop()
        
    except Exception as e:
        print(f"程序启动失败: {e}")
        try:
            messagebox.showerror("启动错误", f"程序启动失败:\n{e}\n\n请检查依赖是否正确安装。")
        except:
            print("无法显示错误对话框")
        sys.exit(1)


if __name__ == '__main__':
    main()