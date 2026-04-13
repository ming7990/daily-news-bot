#!/bin/bash

# 启动早报定时调度器

echo "========================================="
echo "启动早报定时调度器"
echo "========================================="
echo ""
echo "推送时间:"
echo "• 晨报: 每天 09:00"
echo "• 晚报: 每天 18:00"
echo ""
echo "按 Ctrl+C 停止"
echo ""

# 创建日志目录
mkdir -p logs

# 启动调度器
nohup uv run python scheduler.py > logs/scheduler.log 2>&1 &

# 保存PID
echo $! > scheduler.pid

echo "✅ 调度器已启动 (PID: $(cat scheduler.pid))"
echo ""
echo "查看日志: tail -f logs/scheduler.log"
echo "停止调度: kill $(cat scheduler.pid)"
