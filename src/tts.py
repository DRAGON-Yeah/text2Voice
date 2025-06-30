#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文字转语音（TTS）程序
支持中文和英文，优先使用系统内置语音引擎
"""

import sys
import argparse
import logging
import tempfile
import os
import threading
from typing import Optional


def _speak_in_process_macos(args):
    """在独立进程中播放语音的全局函数"""
    text, rate, volume, stop_flag = args
    try:
        import pyttsx3
        import time
        
        # 检查停止标志
        if stop_flag.value == 1:
            return False
        
        # 在新进程中初始化引擎
        engine = pyttsx3.init('nsss')
        if engine is None:
            return False
            
        engine.setProperty('rate', rate)
        engine.setProperty('volume', volume)
        
        # 设置语音
        lang = 'zh' if any('\u4e00' <= char <= '\u9fff' for char in text) else 'en'
        voices = engine.getProperty('voices')
        
        if voices:
            for voice in voices:
                voice_name = voice.name.lower() if hasattr(voice, 'name') else ''
                voice_id = voice.id.lower() if hasattr(voice, 'id') else ''
                
                if lang == 'zh' and ('chinese' in voice_name or 'zh' in voice_id or 'mandarin' in voice_name):
                    engine.setProperty('voice', voice.id)
                    break
                elif lang == 'en' and ('english' in voice_name or 'en' in voice_id or 'american' in voice_name):
                    engine.setProperty('voice', voice.id)
                    break
        
        # 再次检查停止标志
        if stop_flag.value == 1:
            return False
        
        engine.say(text)
        
        # 在播放过程中定期检查停止标志
        def check_stop_during_play():
            start_time = time.time()
            while time.time() - start_time < 30:  # 最多等待30秒
                if stop_flag.value == 1:
                    try:
                        engine.stop()
                    except:
                        pass
                    return False
                time.sleep(0.1)
            return True
        
        import threading
        stop_checker = threading.Thread(target=check_stop_during_play, daemon=True)
        stop_checker.start()
        
        engine.runAndWait()
        return True
        
    except Exception as e:
        print(f"进程中语音播放失败: {e}")
        return False

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None
    print("警告: pyttsx3 未安装，离线语音功能不可用。安装命令: pip install pyttsx3")

try:
    from gtts import gTTS
    import pygame
except ImportError:
    gTTS = None
    pygame = None
    print("警告: gTTS 或 pygame 未安装，在线语音功能不可用。安装命令: pip install gtts pygame")


class TTSEngine:
    """文字转语音引擎类"""
    
    def __init__(self, rate: int = 200, volume: float = 0.9):
        """
        初始化TTS引擎
        
        Args:
            rate: 语速 (words per minute)
            volume: 音量 (0.0-1.0)
        """
        self.rate = rate
        self.volume = volume
        self.offline_engine = None
        self._engine_lock = None
        self._stop_flag = False
        self._init_offline_engine()
    
    def _init_offline_engine(self):
        """初始化离线语音引擎"""
        if pyttsx3 is None:
            logging.warning("pyttsx3 未安装，无法使用离线语音引擎")
            return
        
        try:
            import platform
            
            # 尝试初始化离线引擎
            self.offline_engine = pyttsx3.init()
            
            # 在macOS上使用特殊配置
            if platform.system() == 'Darwin':  # macOS
                # 尝试使用nsss驱动（macOS原生语音）
                try:
                    self.offline_engine = pyttsx3.init('nsss')
                    logging.info("macOS: 使用nsss驱动初始化离线引擎")
                except:
                    # 如果nsss失败，尝试默认驱动
                    try:
                        self.offline_engine = pyttsx3.init()
                        logging.info("macOS: 使用默认驱动初始化离线引擎")
                    except:
                        logging.warning("macOS: 离线引擎初始化失败，将使用在线引擎")
                        self.offline_engine = None
                        return
            
            if self.offline_engine:
                self.offline_engine.setProperty('rate', self.rate)
                self.offline_engine.setProperty('volume', self.volume)
                logging.info("离线语音引擎初始化成功")
                
        except Exception as e:
            logging.error(f"离线语音引擎初始化失败: {e}")
            self.offline_engine = None
    
    def _detect_language(self, text: str) -> str:
        """检测文本语言"""
        # 简单的语言检测：如果包含中文字符则为中文，否则为英文
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                return 'zh'
        return 'en'
    
    def speak_offline(self, text: str) -> bool:
        """使用离线引擎播放语音"""
        if self.offline_engine is None:
            return False
        
        try:
            import platform
            
            # 在macOS上使用进程隔离来避免run loop问题
            if platform.system() == 'Darwin':
                return self._speak_offline_macos(text)
            else:
                return self._speak_offline_other(text)
                
        except Exception as e:
            logging.error(f"离线语音播放失败: {e}")
            return False
    
    def _speak_offline_macos(self, text: str) -> bool:
        """macOS上使用进程隔离播放语音"""
        try:
            import multiprocessing
            import multiprocessing.managers
            
            # 创建一个共享的停止标志
            manager = multiprocessing.Manager()
            stop_flag = manager.Value('i', 0)
            
            # 创建一个进程来监控停止标志
            def monitor_stop_flag():
                while not self._stop_flag:
                    import time
                    time.sleep(0.1)
                stop_flag.value = 1
            
            monitor_thread = threading.Thread(target=monitor_stop_flag, daemon=True)
            monitor_thread.start()
            
            # 使用进程池执行语音播放
            with multiprocessing.Pool(1) as pool:
                result = pool.apply(_speak_in_process_macos, ((text, self.rate, self.volume, stop_flag),))
                return result
                
        except Exception as e:
            logging.warning(f"macOS进程隔离语音播放失败: {e}")
            return False
    
    def _speak_offline_other(self, text: str) -> bool:
        """其他系统的离线语音播放方法"""
        try:
            if self.offline_engine is None:
                return False
                
            # 设置语言相关的语音
            lang = self._detect_language(text)
            voices = self.offline_engine.getProperty('voices')
            
            # 尝试选择合适的语音
            if voices:
                for voice in voices:
                    voice_name = voice.name.lower() if hasattr(voice, 'name') else ''
                    voice_id = voice.id.lower() if hasattr(voice, 'id') else ''
                    
                    if lang == 'zh' and ('chinese' in voice_name or 'zh' in voice_id or 'mandarin' in voice_name):
                        self.offline_engine.setProperty('voice', voice.id)
                        break
                    elif lang == 'en' and ('english' in voice_name or 'en' in voice_id or 'american' in voice_name):
                        self.offline_engine.setProperty('voice', voice.id)
                        break
            
            self.offline_engine.say(text)
            self.offline_engine.runAndWait()
            return True
            
        except Exception as e:
            logging.error(f"其他系统离线语音播放失败: {e}")
            return False
    
    def speak_online(self, text: str) -> bool:
        """使用在线引擎播放语音"""
        if gTTS is None or pygame is None:
            logging.error("gTTS 或 pygame 未安装，无法使用在线语音引擎")
            return False
        
        try:
            # 检测语言
            lang = self._detect_language(text)
            lang_code = 'zh' if lang == 'zh' else 'en'
            
            # 创建临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tmp_filename = tmp_file.name
            
            # 生成语音文件
            tts = gTTS(text=text, lang=lang_code, slow=False)
            tts.save(tmp_filename)
            
            # 播放语音
            pygame.mixer.init()
            pygame.mixer.music.load(tmp_filename)
            pygame.mixer.music.play()
            
            # 等待播放完成
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            # 清理临时文件
            os.unlink(tmp_filename)
            return True
            
        except Exception as e:
            logging.error(f"在线语音播放失败: {e}")
            return False
    
    def speak(self, text: str, force_online: bool = False) -> bool:
        """播放语音（优先离线，失败时使用在线）"""
        if not text.strip():
            logging.warning("输入文本为空")
            return False
        
        # 重置停止标志
        self._stop_flag = False
        
        print(f"[播放语音]: {text}")
        
        # 如果强制使用在线或离线引擎不可用，直接使用在线引擎
        if force_online or self.offline_engine is None:
            return self.speak_online(text)
        
        # 优先尝试离线引擎
        if self.speak_offline(text):
            return True
        
        # 离线失败，尝试在线引擎
        logging.info("离线引擎失败，尝试在线引擎")
        return self.speak_online(text)
    
    def set_rate(self, rate: int):
        """设置语速"""
        self.rate = rate
        if self.offline_engine:
            self.offline_engine.setProperty('rate', rate)
    
    def set_volume(self, volume: float):
        """设置音量"""
        self.volume = max(0.0, min(1.0, volume))
        if self.offline_engine:
            self.offline_engine.setProperty('volume', self.volume)
    
    def stop(self):
        """停止播放"""
        try:
            # 设置停止标志
            self._stop_flag = True
            
            # 停止离线引擎
            if self.offline_engine:
                try:
                    self.offline_engine.stop()
                except:
                    # 某些情况下stop方法可能不可用
                    pass
            
            # 停止pygame播放
            if pygame and pygame.mixer.get_init():
                try:
                    pygame.mixer.stop()
                except:
                    pass
            
            logging.info("语音播放已停止")
            return True
            
        except Exception as e:
            logging.warning(f"停止播放时发生错误: {e}")
            return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='文字转语音程序')
    parser.add_argument('text', nargs='?', help='要转换的文本')
    parser.add_argument('--rate', type=int, default=200, help='语速 (默认: 200)')
    parser.add_argument('--volume', type=float, default=0.9, help='音量 0.0-1.0 (默认: 0.9)')
    parser.add_argument('--online', action='store_true', help='强制使用在线引擎')
    parser.add_argument('--interactive', '-i', action='store_true', help='交互模式')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    # 设置日志级别
    log_level = logging.INFO if args.verbose else logging.WARNING
    logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')
    
    # 初始化TTS引擎
    try:
        tts = TTSEngine(rate=args.rate, volume=args.volume)
    except Exception as e:
        print(f"错误: TTS引擎初始化失败: {e}")
        return 1
    
    # 交互模式
    if args.interactive:
        print("进入交互模式，输入 'quit' 或 'exit' 退出")
        print("支持的命令:")
        print("  :rate <数值>   - 设置语速")
        print("  :volume <数值> - 设置音量")
        print("  :online        - 切换到在线模式")
        print("  :offline       - 切换到离线模式")
        
        force_online = args.online
        
        while True:
            try:
                text = input("请输入文本: ").strip()
                
                if text.lower() in ['quit', 'exit', '退出']:
                    break
                
                if text.startswith(':'):
                    # 处理命令
                    parts = text[1:].split()
                    if not parts:
                        continue
                    
                    cmd = parts[0].lower()
                    if cmd == 'rate' and len(parts) > 1:
                        try:
                            rate = int(parts[1])
                            tts.set_rate(rate)
                            print(f"语速设置为: {rate}")
                        except ValueError:
                            print("错误: 语速必须是数字")
                    elif cmd == 'volume' and len(parts) > 1:
                        try:
                            volume = float(parts[1])
                            tts.set_volume(volume)
                            print(f"音量设置为: {volume}")
                        except ValueError:
                            print("错误: 音量必须是数字")
                    elif cmd == 'online':
                        force_online = True
                        print("切换到在线模式")
                    elif cmd == 'offline':
                        force_online = False
                        print("切换到离线模式")
                    else:
                        print("未知命令")
                    continue
                
                if text:
                    success = tts.speak(text, force_online=force_online)
                    if not success:
                        print("语音播放失败")
                        
            except KeyboardInterrupt:
                print("\n程序被用户中断")
                break
            except EOFError:
                break
        
        return 0
    
    # 单次模式
    elif args.text:
        success = tts.speak(args.text, force_online=args.online)
        if not success:
            print("语音播放失败")
            return 1
        return 0
    
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())