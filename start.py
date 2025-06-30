#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文字转语音程序启动器
让用户选择启动命令行版本或GUI版本
"""

import sys
import subprocess
import os

def show_menu():
    """显示启动菜单"""
    print("=" * 50)
    print("     文字转语音程序启动器")
    print("=" * 50)
    print()
    print("请选择启动模式：")
    print()
    print("1. GUI图形界面 (推荐)")
    print("2. 命令行模式")
    print("3. 功能演示")
    print("4. 查看帮助")
    print("5. 退出")
    print()
    print("=" * 50)

def start_gui():
    """启动GUI版本"""
    print("正在启动GUI图形界面...")
    try:
        subprocess.run(["python3", "gui_tts.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"启动GUI失败: {e}")
    except KeyboardInterrupt:
        print("\n用户中断程序")

def start_cli():
    """启动命令行版本"""
    print("进入命令行交互模式...")
    print("提示：输入 'quit' 或 'exit' 退出")
    print()
    try:
        subprocess.run(["python3", "tts.py", "--interactive"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"启动命令行模式失败: {e}")
    except KeyboardInterrupt:
        print("\n用户中断程序")

def start_demo():
    """启动演示"""
    print("正在运行功能演示...")
    try:
        subprocess.run(["python3", "demo.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"运行演示失败: {e}")
    except KeyboardInterrupt:
        print("\n用户中断程序")

def show_help():
    """显示帮助信息"""
    print()
    print("=" * 60)
    print("                    帮助信息")
    print("=" * 60)
    print()
    print("📋 程序功能：")
    print("   • 将文本转换为语音并播放")
    print("   • 支持中文和英文")
    print("   • 支持语速和音量调整")
    print("   • 提供离线和在线两种引擎")
    print()
    print("🖥️  GUI模式特点：")
    print("   • 图形界面，操作简单")
    print("   • 支持多行文本输入")
    print("   • 实时参数调整")
    print("   • 快捷键支持 (Ctrl+Enter播放, Esc停止)")
    print()
    print("⌨️  命令行模式特点：")
    print("   • 交互式命令行界面")
    print("   • 支持命令行参数")
    print("   • 适合脚本调用")
    print()
    print("🔧 直接使用命令：")
    print("   • GUI模式: python3 gui_tts.py")
    print("   • 命令行: python3 tts.py --interactive")
    print("   • 单次播放: python3 tts.py \"你好世界\"")
    print("   • 查看选项: python3 tts.py --help")
    print()
    print("📦 依赖安装：")
    print("   pip install -r requirements.txt")
    print()
    print("=" * 60)
    print()
    input("按回车键返回主菜单...")

def main():
    """主函数"""
    while True:
        try:
            show_menu()
            choice = input("请输入选项 (1-5): ").strip()
            
            if choice == '1':
                start_gui()
            elif choice == '2':
                start_cli()
            elif choice == '3':
                start_demo()
            elif choice == '4':
                show_help()
            elif choice == '5':
                print("感谢使用文字转语音程序！")
                break
            else:
                print("无效选项，请输入 1-5")
                input("按回车键继续...")
                
        except KeyboardInterrupt:
            print("\n\n感谢使用文字转语音程序！")
            break
        except EOFError:
            print("\n\n感谢使用文字转语音程序！")
            break

if __name__ == '__main__':
    main()