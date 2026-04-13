#!/bin/bash

# 早报定时任务配置脚本
# 配置每日9:00和18:00自动推送早报

# 获取项目绝对路径
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# 创建日志目录
mkdir -p "$PROJECT_DIR/logs"

# 构建crontab条目
CRON_JOB_9AM="0 9 * * * cd $PROJECT_DIR && /usr/bin/uv run python src/main.py '{\"search_query\":\"今日热点\",\"time_range\":\"1d\"}' >> $PROJECT_DIR/logs/morning.log 2>&1"
CRON_JOB_6PM="0 18 * * * cd $PROJECT_DIR && /usr/bin/uv run python src/main.py '{\"search_query\":\"今日热点\",\"time_range\":\"1d\"}' >> $PROJECT_DIR/logs/evening.log 2>&1"

echo "========================================="
echo "早报定时任务配置"
echo "========================================="
echo ""
echo "项目路径: $PROJECT_DIR"
echo ""
echo "即将添加以下定时任务:"
echo "• 每日 9:00 推送早报"
echo "• 每日 18:00 推送早报"
echo ""
echo "日志文件:"
echo "• $PROJECT_DIR/logs/morning.log"
echo "• $PROJECT_DIR/logs/evening.log"
echo ""
read -p "确认添加定时任务吗? (y/n): " confirm

if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
    # 检查是否已有相同的定时任务
    existing_crontab=$(crontab -l 2>/dev/null || echo "")
    
    # 添加新任务
    (echo "$existing_crontab"; echo ""; echo "# 早报推送任务"; echo "$CRON_JOB_9AM"; echo "$CRON_JOB_6PM") | crontab -
    
    echo ""
    echo "✅ 定时任务配置成功!"
    echo ""
    echo "当前crontab内容:"
    crontab -l | grep -A 2 "早报推送任务"
    echo ""
    echo "下次推送时间:"
    echo "• 早上 9:00"
    echo "• 晚上 18:00"
else
    echo ""
    echo "❌ 已取消配置"
fi
