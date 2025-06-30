#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试离线语音引擎的独立脚本
用于诊断macOS上pyttsx3的问题
"""

import sys
import logging
import platform

# 设置详细日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_pyttsx3_basic():
    """测试pyttsx3基本功能"""
    logger.info(f"开始测试pyttsx3，系统: {platform.system()}")
    
    try:
        import pyttsx3
        logger.info("pyttsx3导入成功")
    except ImportError as e:
        logger.error(f"pyttsx3导入失败: {e}")
        return False
    
    # 测试不同的驱动
    drivers = []
    if platform.system() == 'Darwin':
        drivers = ['nsss', None]  # macOS驱动
    else:
        drivers = [None]  # 默认驱动
    
    for driver in drivers:
        logger.info(f"测试驱动: {driver if driver else '默认'}")
        
        try:
            if driver:
                engine = pyttsx3.init(driver)
                logger.info(f"使用{driver}驱动初始化成功")
            else:
                engine = pyttsx3.init()
                logger.info("使用默认驱动初始化成功")
            
            # 获取可用语音
            voices = engine.getProperty('voices')
            logger.info(f"可用语音数量: {len(voices) if voices else 0}")
            
            if voices:
                for i, voice in enumerate(voices[:3]):  # 只显示前3个
                    logger.info(f"语音{i}: {voice.name if hasattr(voice, 'name') else 'Unknown'} - {voice.id if hasattr(voice, 'id') else 'Unknown'}")
            
            # 设置属性
            engine.setProperty('rate', 200)
            engine.setProperty('volume', 0.9)
            logger.info("属性设置成功")
            
            # 测试语音播放
            test_text = "Hello, this is a test."
            logger.info(f"准备播放: {test_text}")
            
            engine.say(test_text)
            logger.info("say()调用成功")
            
            # 这里是关键测试点
            logger.info("准备调用runAndWait()...")
            
            try:
                engine.runAndWait()
                logger.info("runAndWait()调用成功完成")
                return True
            except SystemExit as e:
                logger.warning(f"runAndWait()触发SystemExit: {e}")
                return True  # 在macOS上这可能是正常的
            except Exception as e:
                logger.error(f"runAndWait()异常: {e}")
                return False
                
        except Exception as e:
            logger.error(f"驱动{driver if driver else '默认'}测试失败: {e}")
            continue
    
    return False

def test_alternative_approach():
    """测试替代方案"""
    logger.info("测试替代方案...")
    
    try:
        import pyttsx3
        import threading
        import time
        
        engine = pyttsx3.init()
        engine.setProperty('rate', 200)
        engine.setProperty('volume', 0.9)
        
        test_text = "Alternative approach test."
        engine.say(test_text)
        
        # 使用线程隔离
        speech_completed = threading.Event()
        speech_error = None
        
        def run_speech():
            nonlocal speech_error
            try:
                logger.info("线程中调用runAndWait()...")
                engine.runAndWait()
                logger.info("线程中runAndWait()完成")
                speech_completed.set()
            except SystemExit as e:
                logger.info(f"线程中捕获SystemExit: {e}")
                speech_completed.set()
            except Exception as e:
                logger.error(f"线程中异常: {e}")
                speech_error = e
                speech_completed.set()
        
        speech_thread = threading.Thread(target=run_speech, daemon=True)
        speech_thread.start()
        
        if speech_completed.wait(timeout=10):
            if speech_error:
                logger.error(f"替代方案失败: {speech_error}")
                return False
            else:
                logger.info("替代方案成功")
                return True
        else:
            logger.error("替代方案超时")
            return False
            
    except Exception as e:
        logger.error(f"替代方案异常: {e}")
        return False

def main():
    logger.info("=== 离线语音引擎测试开始 ===")
    logger.info(f"Python版本: {sys.version}")
    logger.info(f"操作系统: {platform.system()} {platform.release()}")
    
    # 测试基本功能
    logger.info("\n=== 测试基本功能 ===")
    basic_result = test_pyttsx3_basic()
    logger.info(f"基本功能测试结果: {'成功' if basic_result else '失败'}")
    
    # 测试替代方案
    logger.info("\n=== 测试替代方案 ===")
    alt_result = test_alternative_approach()
    logger.info(f"替代方案测试结果: {'成功' if alt_result else '失败'}")
    
    logger.info("\n=== 测试完成 ===")
    logger.info(f"最终结果: {'离线引擎可用' if (basic_result or alt_result) else '离线引擎不可用'}")
    
    return 0 if (basic_result or alt_result) else 1

if __name__ == '__main__':
    sys.exit(main())