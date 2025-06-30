#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文字转语音程序入口文件
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 导入主函数
try:
    from tts import main
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保已安装所需依赖: pip install -r requirements.txt")
    sys.exit(1)

if __name__ == '__main__':
    main()