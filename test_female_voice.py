#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试女声语音功能
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.tts import TTSEngine
import time

def test_female_voice():
    """测试女声语音"""
    print("=== 测试女声语音功能 ===")
    
    # 初始化TTS引擎
    tts = TTSEngine(rate=180, volume=0.8)
    
    # 测试中文女声
    print("\n1. 测试中文女声...")
    chinese_text = "你好，我是婷婷，很高兴为您服务。这是中文女声测试。"
    success = tts.speak_offline(chinese_text)
    print(f"中文女声播放结果: {'成功' if success else '失败'}")
    
    time.sleep(1)
    
    # 测试英文女声
    print("\n2. 测试英文女声...")
    english_text = "Hello, I am Samantha. This is a test of English female voice."
    success = tts.speak_offline(english_text)
    print(f"英文女声播放结果: {'成功' if success else '失败'}")
    
    time.sleep(1)
    
    # 显示当前使用的语音信息
    print("\n3. 检查当前语音设置...")
    try:
        if tts.offline_engine:
            current_voice = tts.offline_engine.getProperty('voice')
            voices = tts.offline_engine.getProperty('voices')
            
            for voice in voices:
                if voice.id == current_voice:
                    gender = getattr(voice, 'gender', 'unknown')
                    print(f"当前语音: {voice.name} (ID: {voice.id})")
                    print(f"性别: {gender}")
                    break
    except Exception as e:
        print(f"获取语音信息失败: {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_female_voice()