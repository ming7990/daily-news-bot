#!/usr/bin/env python3
"""
早报定时调度器
在9:00和18:00自动推送早报
"""

import schedule
import time
import json
import logging
import os
import subprocess
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/scheduler.log')
    ]
)
logger = logging.getLogger(__name__)


def push_news():
    """推送早报"""
    logger.info(f"开始推送早报... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        # 使用subprocess调用uv run
        result = subprocess.run(
            ['uv', 'run', 'python', 'src/main.py', '-m', 'flow', '-i', '{"search_query":"今日热点","time_range":"1d"}'],
            capture_output=True,
            text=True,
            cwd='/workspace/projects'
        )
        if result.returncode == 0:
            logger.info(f"早报推送成功")
            logger.info(f"推送结果: {result.stdout[:500]}")  # 只记录前500字符
        else:
            logger.error(f"早报推送失败: {result.stderr}")
    except Exception as e:
        logger.error(f"早报推送异常: {e}")


def run_scheduler():
    """运行调度器"""
    # 创建日志目录
    os.makedirs('logs', exist_ok=True)

    # 设置定时任务
    schedule.every().day.at("09:00").do(push_news)
    schedule.every().day.at("18:00").do(push_news)

    logger.info("=" * 50)
    logger.info("早报定时调度器已启动")
    logger.info("=" * 50)
    logger.info("推送时间:")
    logger.info("• 晨报: 每天 09:00")
    logger.info("• 晚报: 每天 18:00")
    logger.info("当前时间: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("=" * 50)

    # 持续运行
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次


if __name__ == "__main__":
    run_scheduler()
