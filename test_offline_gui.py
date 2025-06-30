#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试离线引擎在GUI环境中的工作情况
"""

import sys
import os
import logging

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tts import TTSEngine

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_offline_engine():
    """测试离线引擎"""
    logger.info("开始测试离线引擎...")
    
    try:
        # 初始化TTS引擎
        tts = TTSEngine()
        logger.info("TTS引擎初始化成功")
        
        # 检查离线引擎状态
        if tts.offline_engine is None:
            logger.warning("离线引擎不可用")
            return False
        else:
            logger.info("离线引擎可用")
        
        # 测试中文语音
        logger.info("测试中文语音...")
        success1 = tts.speak_offline("你好，这是离线引擎测试")
        logger.info(f"中文语音测试结果: {'成功' if success1 else '失败'}")
        
        # 测试英文语音
        logger.info("测试英文语音...")
        success2 = tts.speak_offline("Hello, this is offline engine test")
        logger.info(f"英文语音测试结果: {'成功' if success2 else '失败'}")
        
        # 测试自动选择模式
        logger.info("测试自动选择模式...")
        success3 = tts.speak("自动选择引擎测试", force_online=False)
        logger.info(f"自动选择模式测试结果: {'成功' if success3 else '失败'}")
        
        return success1 and success2 and success3
        
    except Exception as e:
        logger.error(f"测试过程中发生错误: {e}")
        return False

def main():
    logger.info("=== 离线引擎GUI环境测试 ===")
    
    result = test_offline_engine()
    
    logger.info(f"\n=== 测试完成 ===")
    logger.info(f"最终结果: {'离线引擎在GUI环境中工作正常' if result else '离线引擎在GUI环境中存在问题'}")
    
    return 0 if result else 1

if __name__ == '__main__':
    sys.exit(main())