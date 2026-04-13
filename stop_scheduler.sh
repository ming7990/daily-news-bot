#!/bin/bash

# 停止早报定时调度器

if [ -f scheduler.pid ]; then
    PID=$(cat scheduler.pid)
    if ps -p $PID > /dev/null 2>&1; then
        kill $PID
        rm scheduler.pid
        echo "✅ 调度器已停止"
    else
        echo "⚠️  调度器未在运行"
        rm -f scheduler.pid
    fi
else
    echo "⚠️  未找到调度器PID文件"
    # 尝试查找并停止
    pkill -f "scheduler.py" && echo "✅ 已停止调度器进程" || echo "❌ 未找到运行中的调度器"
fi
