#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文字转语音程序演示脚本
"""

import subprocess
import time
import sys

def run_tts(text, *args):
    """运行TTS程序"""
    cmd = ["python3", "tts.py", text] + list(args)
    print(f"\n执行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(f"输出: {result.stdout.strip()}")
    if result.stderr:
        print(f"错误: {result.stderr.strip()}")
    return result.returncode == 0

def main():
    """演示主函数"""
    print("=" * 60)
    print("文字转语音（TTS）程序演示")
    print("=" * 60)
    
    demos = [
        ("基本中文语音", ["你好，欢迎使用文字转语音程序！"]),
        ("基本英文语音", ["Hello, welcome to the text-to-speech program!"]),
        ("调整语速（慢速）", ["这是一个慢速语音测试", "--rate", "100"]),
        ("调整语速（快速）", ["这是一个快速语音测试", "--rate", "300"]),
        ("调整音量", ["这是音量测试", "--volume", "0.5"]),
        ("在线引擎测试", ["测试在线语音引擎", "--online"]),
        ("中英文混合", ["Hello你好，这是中英文混合测试"]),
    ]
    
    for i, (desc, args) in enumerate(demos, 1):
        print(f"\n{i}. {desc}")
        print("-" * 40)
        
        success = run_tts(*args)
        if not success:
            print("❌ 执行失败")
        else:
            print("✅ 执行成功")
        
        # 等待一下再执行下一个
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("\n要进入交互模式，请运行：")
    print("python3 tts.py --interactive")
    print("=" * 60)

if __name__ == '__main__':
    main()