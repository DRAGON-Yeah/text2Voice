#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试停止播放功能
"""

import sys
import os
import time
import threading

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tts import TTSEngine

def test_stop_function():
    """测试停止播放功能"""
    print("=== 测试停止播放功能 ===")
    
    # 初始化TTS引擎
    tts_engine = TTSEngine()
    
    if not tts_engine.offline_engine:
        print("离线引擎不可用，无法测试停止功能")
        return
    
    print("离线引擎可用")
    
    # 测试1: 播放长文本并在中途停止
    print("\n测试1: 播放长文本并在中途停止...")
    long_text = "这是一个很长的测试文本，用来测试停止播放功能是否正常工作。" * 5
    
    # 在新线程中播放语音
    def play_long_text():
        result = tts_engine.speak(long_text, force_online=False)
        print(f"长文本播放结果: {'成功' if result else '失败'}")
    
    play_thread = threading.Thread(target=play_long_text, daemon=True)
    play_thread.start()
    
    # 等待2秒后停止播放
    time.sleep(2)
    print("正在停止播放...")
    stop_result = tts_engine.stop()
    print(f"停止播放结果: {'成功' if stop_result else '失败'}")
    
    # 等待播放线程结束
    play_thread.join(timeout=5)
    
    # 测试2: 停止后重新播放
    print("\n测试2: 停止后重新播放...")
    time.sleep(1)
    result2 = tts_engine.speak("停止后重新播放测试", force_online=False)
    print(f"重新播放结果: {'成功' if result2 else '失败'}")
    
    print("\n=== 停止功能测试完成 ===")

if __name__ == "__main__":
    test_stop_function()